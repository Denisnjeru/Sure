from rest_framework import pagination
from rest_framework.response import Response

class PageNumberPagination(pagination.PageNumberPagination):
    # page_size = 10
    page_size_query_param = "page_size"

    ##
    # Returns the paginated Response.
    #
    # @param data The data that is to be displayed
    #
    # @return The paginated Response.
    #
    def get_paginated_response(self, data):
        return Response({
            "links":  {
                "next":     self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "count":      self.page.paginator.count,
            "results":    data,
            "pageCount":  self.page.paginator.num_pages,
            "pageNumber": self.page.number,
            "pageSize":   self.page.paginator.per_page
        })
