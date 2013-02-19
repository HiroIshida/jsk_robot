#!/usr/bin/env python

import roslib
roslib.load_manifest('jsk_pr2_startup')
import rospy
import twoauth,yaml,sys
import re, os
from std_msgs.msg import String

# see http://d.hatena.ne.jp/gumilab/20101004/1286154912 to setup CKEY/AKEY
try:
    key = yaml.load(open('/var/lib/robot/twitter_acount_pr2jsk.yaml'))
    CKEY = key['CKEY']
    CSECRET = key['CSECRET']
    AKEY = key['AKEY']
    ASECRET = key['ASECRET']
except IOError as e:
    rospy.logerr('"/var/lib/robot/twitter_acount_pr2jsk.yaml" not found')
    rospy.logerr("$ rosrun python_twoauth get_access_token.py")
    rospy.logerr("cat /var/lib/robot/twitter_acount_pr2jsk.yaml <<EOF")
    rospy.logerr("CKEY: xxx")
    rospy.logerr("CSECRET: xxx")
    rospy.logerr("AKEY: xxx")
    rospy.logerr("ASECRET: xxx")
    rospy.logerr("EOF")
    rospy.logerr('see http://d.hatena.ne.jp/gumilab/20101004/1286154912 for detail')
    sys.exit(-1)

def twit(dat):
    message = dat.data
    rospy.loginfo(rospy.get_name()+" sending %s",message)
    # search word start from / and end with {.jpeg,.jpg,.png,.gif}
    m = re.search('/\S+\.(jpeg|jpg|png|gif)', message)
    if m :
        filename = m.group(0)
        message = re.sub(filename,"",message)
        if os.path.exists(filename):
            twitter.status_update_with_media(message, filename)
            return
    twitter.status_update(message)

if __name__ == '__main__':
    twitter = twoauth.api(CKEY, CSECRET, AKEY, ASECRET)
    rospy.init_node('rostwitter', anonymous=True)
    rospy.Subscriber("pr2twit", String, twit)
    rospy.spin()
