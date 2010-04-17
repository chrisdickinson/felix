import optparse
import simplejson
import os
import sys

def create_superuser():
    parser = optparse.OptionParser()
    parser.add_option('-k', '--key', dest='key', metavar='KEY', help='an optional id_rsa.pub to use')
    options, args = parser.parse_args()
    username = args[0]
    key = None
    if options.key:
        key_file = os.path.expanduser(options.key)
        if os.path.isfile(key_file):
            with open(key_file) as input:
                key = input.read() 
        else:
            print >>sys.stderr, "%s does not exist." % options.key
    else:
        key = sys.stdin.read()

    output_dict = {
        'users':{
            username:{
                'auth':{
                    'adduser':True,
                    'modifyuser':True,
                },
                'keys':[key.strip(),],
            }
        }
    }
    print simplejson.dumps(output_dict)

if __name__ == '__main__':
    create_superuser()
