from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core
from mitmproxy.addons import block
from mitmproxy import http

####################################################################################################
https://stackoverflow.com/questions/57178896/how-to-shutdown-dumpmaster-mitmproxy-programmatically
####################################################################################################
class AdjustBody:
    def response(self, flow: http.HTTPFlow) -> None:
        if "holdout" in flow.request.url:
            print("[CATCH IT !!!]: %s" % flow.request.url)
            #print("[CATCH IT !!!]: %s" % flow.response.text)

add_on = AdjustBody()

opts = options.Options(listen_host='192.168.1.12', listen_port=8080)
pconf = proxy.config.ProxyConfig(opts)

m = DumpMaster(opts)
m.options.set('block_global=false')
m.server = proxy.server.ProxyServer(pconf)
m.addons.add(add_on)

try:
    m.run()
except KeyboardInterrupt:
    m.shutdown()
    
################################## Output is like below ######################################
192.168.1.6:65471: clientdisconnect
192.168.1.6:65473: clientconnect
192.168.1.6:65444: GET https://iphone-xml.booking.com/json/mobile.getFeaturedReviews?i_am_from=nl&user_latitude=31.19218529879378&device_id=645a24304331451a969c06987c823719&user_longitude=121.3820137884517&affiliate_id=331867&languagecode=en-us&user_version=24.1-iphone&hotel_id=6242328&network_type=wifi&user_os=13.2.3&auth_token=37279858147c704f2d7aaef969dd5b506c20df79&exp_pset_multi_bucket_app=2&exp_disable_bsd_holdout=1
                << 200 OK 58b
[CATCH IT !!!]: https://iphone-xml.booking.com/json/mobile.getFeaturedReviews?i_am_from=nl&user_latitude=31.19218529879378&device_id=645a24304331451a969c06987c823719&user_longitude=121.3820137884517&affiliate_id=331867&languagecode=en-us&user_version=24.1-iphone&hotel_id=6242328&network_type=wifi&user_os=13.2.3&auth_token=37279858147c704f2d7aaef969dd5b506c20df79&exp_pset_multi_bucket_app=2&exp_disable_bsd_holdout=1
192.168.1.6:65474: clientconnect
192.168.1.6:65447: GET https://iphone-xml.booking.com/json/bookings.getHotelReviewScores?include_wifi_score=1&user_os=13.2.3&hotel_ids=6242328&affiliate_id=331867&auth_token=37279858147c704f2d7aaef969dd5b506c20df79&user_version=24.1-iphone&network_type=wifi&customer_type=total&user_latitude=31.19218529879378&languagecode=en-us&i_am_from=nl&device_id=645a24304331451a969c06987c823719&include_breakfast_score=1&user_longitude=121.3820137884517&use_original_question_id=1&exp_disable_bsd_holdout=1&exp_pset_multi_bucket_app=2
                << 200 OK 471b


