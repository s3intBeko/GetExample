from Curl import Curl

_curl = Curl()
def _get():
    #_curl._encoding('gzip')
    _curl.set_httpheader([
            'Content-Type: application/x-www-form-urlencoded',
            'Connection: Keep-Alive',
            'Accept-Encoding: gzip'
        ])

    try:
        _curl.get("http://192.168.0.1/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=DISCONNECT_NETWORK")
    except Exception as err:
        print("ERRROR")
        print(err)
    
    print(_curl.result)
    

_get()