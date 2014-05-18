import boto.mturk.connection as conn
from boto.mturk.price import Price
import time
import sys

qualified_workers = ['A248D5XVN1YGCZ', 'A2QAJ8BJ5QBB9A', 'A2WRSEO8HQRG5K', 'A37P0EXFVTAP0D', 'A38KIO2400LOTJ', 'A3DY78Q4FCWTXX', 'A3N87BX6PS0SIB', 'A9XWAWNLJN8DA']
action_annotation_type_id = '276M25L8I9N3M15OL9FEFQW7T8OIS7'
lines = open('mturk_keys').read().splitlines()

def new_mturk_connection():
    return conn.MTurkConnection(aws_access_key_id=lines[0], aws_secret_access_key=lines[1], is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)

def pay_bonus(mturk, worker_id, assignment_id, amount, reason):
  print 'paying $' + str(amount) + ' to worker ' + worker_id + '...',
  sys.stdout.flush()
  time.sleep(5.0)
  mturk.grant_bonus(worker_id, assignment_id, Price(amount), reason)
  print 'success!'

def get_all_reviewable_hits(mtc):
    page_size = 50
    hits = mtc.get_reviewable_hits(page_size=page_size)
    print "Total results to fetch %s " % hits.TotalNumResults
    print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        print "Request hits page %i" % pn
        temp_hits = mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
    return hits
