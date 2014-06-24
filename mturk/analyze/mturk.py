import boto.mturk.connection as conn

qualified_workers = ['A248D5XVN1YGCZ', 'A2QAJ8BJ5QBB9A', 'A2WRSEO8HQRG5K', 'A37P0EXFVTAP0D', 'A38KIO2400LOTJ', 'A3DY78Q4FCWTXX', 'A3N87BX6PS0SIB', 'A9XWAWNLJN8DA']
action_annotation_type_id = '276M25L8I9N3M15OL9FEFQW7T8OIS7'
f = open('mturk_keys','r')
access_key = f.readline()
secret_key = f.readline()
def new_mturk_connection():
    return conn.MTurkConnection(aws_access_key_id=access_key, aws_secret_access_key=secret_key, is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)

