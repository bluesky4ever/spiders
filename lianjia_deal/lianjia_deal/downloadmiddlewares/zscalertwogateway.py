class zscalertwoGateway(object):
    def process_request(self, request, spider):
        return None
    
    def process_response(self, request, response, spider):
        print("gateway: Process_response")
        print(response.url," : ", response.status)
        return response
#        res = None
#        if response.url.find('gateway.zscalertwo.net:443') >=0:
#            if response.status == 200:
#                res = response.replace(status=307)
#                print("return new res")
#                return res

    def process_exception(self, request, exception, spider):
        return None
    