# -*- coding:utf-8 -*-
import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def show_train_info(train):
    if train:
        code_map = train['codeMap']
        txt = train['station_train_code'] + '('+train['train_no']+'): ' + \
              code_map[train['from_station_telecode']]+'('+train['start_time']+')->'+code_map[train['to_station_telecode']]+'('+train['arrive_time']+'), '+ '历时'+train['lishi']+', '+ \
              (u'可买' if train['canWebBuy'] == 'Y' else u'售完') + ', ' + \
              '(' + get_seat_name('zy_num') + ':' + str(train['zy_num']) + ',' + get_seat_name('ze_num') + ':' + str(train['ze_num']) + ',' + get_seat_name('wz_num') + ':' + str(train['wz_num']) + ')'
        print txt


def get_seat_name(seat):
    name_map = {
        'gg_num': 'x',
        'gr_num': '高级软卧',
        'qt_num': '其他',
        'rw_num': '软卧',
        'rz_num': '软座',
        'tz_num': 'x',
        'wz_num': '无座',
        'yb_num': 'x',
        'yw_num': '硬卧',
        'yz_num': '硬座',
        'ze_num': '二等座',
        'zy_num': '一等座',
        'swz_num': '商务座/特等座',
        'srrb_num': 'x'
    }
    return name_map[seat] if name_map[seat] else ''


def query_train_info(date, from_where, to_where):
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Mobile Safari/537.36'
    my_headers = {'User - Agent': user_agent}
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+from_where+'&leftTicketDTO.to_station='+to_where+'&purpose_codes=ADULT'
    request = urllib2.Request(url=url, headers=my_headers)
    response = urllib2.urlopen(request)
    data = response.read()
    # print data
    data_obj = json.loads(data, encoding='utf-8')
    data = data_obj['data']
    map = data['map']
    result_list = data['result']
    for result in result_list:
        result = result.split('|')
        train = {
                    'codeMap': map,
                    'secretStr': result[0],
                    'train_no': result[2], # train inner code
                    'station_train_code': result[3], # train name
                    'from_station_telecode': result[6],
                    'to_station_telecode': result[7],
                    'start_time': result[8],
                    'arrive_time': result[9],
                    'lishi': result[10],
                    'canWebBuy': result[11],
                    'gg_num': result[20] if result[20] else 0,
                    'gr_num': result[21] if result[21] else 0,
                    'qt_num': result[22] if result[22] else 0,
                    'rw_num': result[23] if result[23] else 0,
                    'rz_num': result[24] if result[24] else 0,
                    'tz_num': result[25] if result[25] else 0,
                    'wz_num': result[26] if result[26] else 0,
                    'yb_num': result[27] if result[27] else 0,
                    'yw_num': result[28] if result[28] else 0,
                    'yz_num': result[29] if result[29] else 0,
                    'ze_num': result[30] if result[30] else 0,
                    'zy_num': result[31] if result[31] else 0,
                    'swz_num': result[32] if result[32] else 0,
                    'srrb_num': result[33] if result[33] else 0
        }
        show_train_info(train)


def get_train_info(date=None, from_w=None, to_w=None):
    date = date if date else '2018-09-18'
    from_w = from_w if from_w else 'HZH'
    to_w = to_w if to_w else 'BJP'
    query_train_info(date, from_w, to_w)


if __name__ == '__main__':
    get_train_info()
