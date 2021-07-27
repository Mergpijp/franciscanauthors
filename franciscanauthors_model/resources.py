from import_export import resources
from .models import Author
import re
import sys

class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author

    def regular_expression(self):
        _illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F),
                            (0x7F, 0x84), (0x86, 0x9F),
                            (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)]
        if sys.maxunicode >= 0x10000:  # not narrow build
            _illegal_unichrs.extend([(0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
                                     (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF),
                                     (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
                                     (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                                     (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF),
                                     (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
                                     (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                                     (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)])

        _illegal_ranges = ["%s-%s" % (chr(low), chr(high))
                           for (low, high) in _illegal_unichrs]
        _illegal_xml_chars_RE = re.compile(u'[%s]' % u''.join(_illegal_ranges))

        return _illegal_xml_chars_RE

    def dehydrate_author_name(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        clean = _illegal_xml_chars_RE.sub('', author.author_name)
        return clean

    def dehydrate_biography(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        clean = _illegal_xml_chars_RE.sub('', author.biography)
        return clean

    def dehydrate_affiliation(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        clean = _illegal_xml_chars_RE.sub('', author.affiliation)
        return clean

    def dehydrate_works_author_list(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        for idx, work in enumerate(author.works_author_list.all()):
            author.works_author_list[idx].text = _illegal_xml_chars_RE.sub('', author.works_author_list[idx].text)
            author.works_author_list[idx].title = _illegal_xml_chars_RE.sub('', author.works_author_list[idx].title)
            author.works_author_list[idx].publisher = _illegal_xml_chars_RE.sub('', author.works_author_list[idx].publisher)
            author.works_author_list[idx].location = _illegal_xml_chars_RE.sub('', author.works_author_list[idx].location)
            author.works_author_list[idx].detail_descriptions = _illegal_xml_chars_RE.sub('', author.works_author_list[idx].detail_descriptions)
        return author.works_author_list

    def dehydrate_alias_list(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        for idx, work in enumerate(author.alias_list.all()):
            author.alias_list[idx].alias = _illegal_xml_chars_RE.sub('', author.alias_list[idx].alias)
        return author.alias_list

    def dehydrate_additional_info_list(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        for idx, work in enumerate(author.additional_info_list.all()):
            author.additional_info_list[idx].add_comments = _illegal_xml_chars_RE.sub('', author.additional_info_list[idx].add_comments)
        return author.additional_info_list

    def dehydrate_location_time_list(self, author):
        _illegal_xml_chars_RE = self.regular_expression()
        for idx, work in enumerate(author.dehydrate_location_time_list.all()):
            author.dehydrate_location_time_list[idx].geo_location_name = _illegal_xml_chars_RE.sub('', author.dehydrate_location_time_list[idx].geo_location_name)
            author.dehydrate_location_time_list[idx].fr_province = _illegal_xml_chars_RE.sub('',
                                                                                      author.dehydrate_location_time_list[
                                                                                          idx].fr_province)
            author.dehydrate_location_time_list[idx].date = _illegal_xml_chars_RE.sub('',
                                                                                      author.dehydrate_location_time_list[
                                                                                          idx].date)
        return author.dehydrate_location_time_list
