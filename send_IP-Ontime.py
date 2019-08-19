import urllib.request
import requests
import ctypes, os

def get_ip_address():
    """
    get your global IP address(IPv4)

    Parameters
    ----------

    Returns
    ----------
    get_ip:string
        string of IP address
    """
    #get_ip = urllib.request.urlopen('http://ipcheck.ieserver.net').read().decode('utf-8')
    temp = urllib.request.urlopen("http://checkip.dyndns.org").read().decode("utf-8")
    get_ip = temp.rsplit(":", 1)[1].rsplit("</body>", 1)[0]
    return(get_ip)


def post_line(send_message):
    """
    send message to LINE_notify

    Parameters
    ----------
    send_message:string
        string to send to LINE_notify

    Returns
    ---------
    """
    line_notify_token = 'Your access token'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = send_message
    payload = {'message': message}

    #create headers
    headers = {'Authorization': 'Bearer ' + line_notify_token}

    #send message
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)


#This program can get monotonic time durations of your computer.
#I found this from 'stackoverflow.com'
#https://stackoverflow.com/questions/1205722/how-do-i-get-monotonic-time-durations-in-python

CLOCK_MONOTONIC_RAW = 4 # see <linux/time.h>

class timespec(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]

librt = ctypes.CDLL('librt.so.1', use_errno=True)
clock_gettime = librt.clock_gettime
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

def monotonic_time():
    t = timespec()
    if clock_gettime(CLOCK_MONOTONIC_RAW , ctypes.pointer(t)) != 0:
        errno_ = ctypes.get_errno()
        raise OSError(errno_, os.strerror(errno_))
    return t.tv_sec + t.tv_nsec * 1e-9



def main():
    # get a string of your Ip address
    # and delete <LF> code from this string
    r_ip=get_ip_address().rstrip()

    # get monotonic time durations of your computer
    r_day=round(monotonic_time()/(60*60*24), 1)

    r_mes='\nIP:'+r_ip+'\n起動:'+str(r_day)+'日'

    #send IP address to LINE_notify
    post_line(r_mes)


if __name__ == "__main__":
    main()
