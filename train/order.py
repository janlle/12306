# coding:utf8

import json
import re
from train.search_stack import *
import config.urls as urls
import tickst_config as config
import util.app_util as util
from util.net_util import api
from train.passenger import Passenger
from util.logger import Logger

log = Logger(__name__)

headers = {
    "Cookie": "JSESSIONID=E9F3801DA0FF6BDBA5C9BD5F3C24B73F; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u6B66%u660C%2CWCN; _jc_save_toStation=%u957F%u6C99%2CCSQ; _jc_save_fromDate=2019-10-25; _jc_save_toDate=2019-09-30; BIGipServerotn=653263370.24610.0000; RAIL_EXPIRATION=1570596001182; RAIL_DEVICEID=QpBR0-Dv71ZjiueC0I29kqdexiMb1hpE6Wbq-e29e4f7z05D9MvtlaP8tyfVRzQcGEumaHWSRkACeCQm2FfxMPZWpwTWHAm1Yli-8I_uAMnrAh4d-Pxx6O0iqh2o6H4G1fD-dn5F8Xgccjh0fs1M-EqVSFsA82qq; route=6f50b51faa11b987e576cdb301e545c4"
}


class Order(object):

    def __init__(self):
        self.order_url = urls.URLS.get('submit_order')
        self.passenger = urls.URLS.get('passenger_url')
        self.check_order_info = urls.URLS.get('check_order_info')
        self.confirm_passenger = urls.URLS.get('confirm_passenger')

    def submit(self, ticket, passenger_name, seat_type):
        """提交车票信息"""
        submit_url = self.order_url.get('request_url')
        ticket_params = self.order_url.get('params')
        ticket_params['back_train_date'] = util.current_date()
        ticket_params['train_date'] = config.DATE
        ticket_params['secretStr'] = util.decode_secret_str(ticket.secret_str)
        ticket_params['query_from_station_name'] = ticket.from_station
        ticket_params['query_to_station_name'] = ticket.to_station
        submit_order_response = api.post(submit_url, ticket_params, headers=headers)
        if submit_order_response.status_code == 200 and submit_order_response.json()['httpstatus'] == 200:
            print(submit_order_response.json())
            self.check_order_info(passenger_name, seat_type)
        else:
            log.info('submit order error')

    def check_order(self, passenger_name, seat_type):
        """
        :return:
        """
        # get submit params
        submit_token = self.get_submit_token()

        # get passenger
        passenger = self.get_passenger(passenger_name)

        request_url = self.check_order_info.get('request_url')
        request_params = self.check_order_info.get('params')
        request_params['passengerTicketStr'] = passenger[0].passenger_ticket_str(seat_type)
        request_params['oldPassengerStr'] = passenger[0].old_passenger_str()
        request_params['REPEAT_SUBMIT_TOKEN'] = submit_token['repeat_submit_token']

        api.post(request_url, body=request_params, headers=headers)
        pass

    def get_passenger(self, name=None):
        """
        get account added passenger
        :param name:
        :return:
        """
        request_url = self.passenger.get('request_url')
        request_params = self.passenger.get('params')
        passengers_data = api.post(request_url, request_params, headers=headers)
        if passengers_data.status_code == 200:
            passengers = passengers_data.json()['data']['normal_passengers']
            if passengers and len(passengers) > 0:
                passengers_list = []
                for p in passengers:
                    i = Passenger()
                    i.passenger_name = p['passenger_name']
                    i.sex_code = p['sex_code']
                    i.sex_name = p['sex_name']
                    i.born_date = p['born_date']
                    i.country_code = p['country_code']
                    i.passenger_id_type_code = p['passenger_id_type_code']
                    i.passenger_id_type_name = p['passenger_id_type_name']
                    i.passenger_id_no = p['passenger_id_no']
                    i.passenger_type = p['passenger_type']
                    i.passenger_flag = p['passenger_flag']
                    i.passenger_type_name = p['passenger_type_name']
                    i.mobile_no = p['mobile_no']
                    i.phone_no = p['phone_no']
                    i.email = p['email']
                    i.first_letter = p['first_letter']
                    i.total_times = p['total_times']
                    i.index_id = p['index_id']
                    i.all_enc_str = p['allEncStr']
                    passengers_list.append(i)
                if name:
                    return list(filter(lambda passenger: passenger.passenger_name == name, passengers_list))
                else:
                    return passengers_list

    def get_submit_token(self):
        """
        get submit ticket token from confirm passenger page
        :return:
        """
        url = self.confirm_passenger.get('request_url')
        html_page = api.get(url, headers=headers)
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>中国铁路12306</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link href="/otn/resources/css/validation.css" rel="stylesheet" />
<link href="/otn/resources/merged/common_css.css?cssVersion=1.9054" rel="stylesheet" />
<link rel="icon" href="/otn/resources/images/ots/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/otn/resources/images/ots/favicon.ico" type="image/x-icon" />
<script>
/*<![CDATA[*/
 var ctx='/otn/';
 var globalRepeatSubmitToken = '7e1de7e5f925b446cad05ad7fd341f2a';
 var global_lang = 'zh_CN';
 var sessionInit = '\u52A0\u91D1\u5B89';
 var isShowNotice = null;
 var CLeftTicketUrl = null;
 var isTestFlow = null;
 var isMobileCheck = null;
 var passport_appId = null;
 var passport_login = null;
 var passport_captcha = null;
 var passport_authuam = null;
 var passport_captcha_check = null;
 var passport_authclient = null;
 var passport_loginPage = null;
 var passport_okPage = null;
 var passport_proxy_captcha =  null;
 /*]]>*/
</script>
<script src="/otn/resources/merged/common_js.js?scriptVersion=1.9156" type="text/javascript"></script>
<!-- js i18n -->
<!-- jquery validation i18n -->
<!-- head and footer -->
<script src="/otn/HttpZF/GetJS" type="text/javascript"></script>
<link href="/otn/resources/merged/passengerInfo_css.css?cssVersion=1.9054" rel="stylesheet" />
<script type="text/javascript" src="/otn/resources/merged/passengerInfo_js.js?scriptVersion=1.9156" xml:space="preserve"></script>
</head>
<script src="/otn/dynamicJs/oxmhuml" type="text/javascript" xml:space="preserve"></script>
<script xml:space="preserve">

/*<![CDATA[*/
 var id_type_code = '1';
 var isDw='N';
 var checkTrain=null;
 var isLimitTran='N';
 var CHANGETSFLAG=null;
 var canInsurance=true;
 var queryOrderWaitTimeInterval='3000';
 var canChooseSeats=null;
 var choose_Seats=null;
 var canChooseBeds=null;
 var isCanChooseMid=null;
 var trms_train_flag=null;
 var trmsDetail=null;
 var trmsDetailAll=null;
 var price_info_trms=null;
 /*]]>*/
</script>
<body id="body_id"><div id="dialog_fczk" style="display: none;"><div class="mark"></div>
<div class="up-box w600"><div class="up-box-hd">温馨提示<a href="javascript:" id="dialog_fczk_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd"><div class="up-con clearfix"><span class="icon i-opt"></span>
<div class="r-txt"><div class="tit">购买往返优惠票的旅客，不得单独办理往程车票的退票业务。是否继续?</div>
</div>
</div>
<div class="lay-btn"><a href="javascript:" id="dialog_fczk_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="dialog_fczk_ok" class="btn92s" shape="rect">确认</a>
</div>
</div>
</div>
</div>
<div id="dialog_smoker" style="display: none;"><div class="mark"></div>
<div class="up-box w600"><div class="up-box-hd">温馨提示<a href="javascript:" id="dialog_smoker_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd"><div class="up-con clearfix"><span class="icon i-opt"></span>
<div class="r-txt"><div class="tit" id="dialog_smoker_msg"></div>
</div>
</div>
<div class="lay-btn"><a href="javascript:" id="dialog_smoker_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="dialog_smoker_ok" class="btn92s" shape="rect">确定</a>
</div>
</div>
</div>
</div>
<div id="dialog_xsertcj" style="display: none;"><div class="mark"></div>
<div class="up-box w600"><div class="up-box-hd">温馨提示<a href="javascript:" id="dialog_xsertcj_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd"><div class="up-con clearfix"><span class="icon i-opt"></span>
<div class="r-txt"><div class="tit" id="dialog_xsertcj_msg"></div>
</div>
</div>
<div class="lay-btn"><a href="javascript:" id="dialog_xsertcj_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="dialog_xsertcj_ok" class="btn92s" shape="rect">确认</a>
</div>
</div>
</div>
</div>
<div id="trms_dg" style="display: none;"><div class="mark"></div>
<div class="up-box w600"><div class="up-box-hd">温馨提示<a href="javascript:" id="trms_dg_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd"><div class="up-con clearfix"><span class="icon i-opt"></span>
<div class="r-txt"><div class="tit" id="trms_dg_msg"></div>
</div>
</div>
<div class="lay-btn"><a href="javascript:" id="trms_dg_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="trms_dg_ok" class="btn92s" shape="rect">确认</a>
</div>
</div>
</div>
</div>
<div id="dialog_add" style="display: none;"><div class="mark"></div>
<div class="up-box" style="width:640px;"><div class="up-box-hd">新增乘客<a href="javascript:" id="dialog_add_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd" style="padding:15px 10px;border:1px solid #298CCE;"><table class="per-ticket" style="margin-left:0px;"><tr><th style="text-align:center;" rowspan="1" colspan="1">票种</th>
<th style="text-align:center;" rowspan="1" colspan="1">姓名</th>
<th style="text-align:center;" rowspan="1" colspan="1">证件类型</th>
<th style="text-align:center;" rowspan="1" colspan="1">证件号码</th>
<th style="text-align:center;" rowspan="1" colspan="1">国家/地区</th>
</tr>
<tbody id="showaddpassenger"><tr><td rowspan="1" colspan="1"><select id="ptypeselect"></select>
</td>
<td rowspan="1" colspan="1"><div><input id="pname_value" class="inptxt w110" type="text" />
</div>
</td>
<td rowspan="1" colspan="1"><select id="typeselect" class="w110"></select>
</td>
<td rowspan="1" colspan="1"><input id="pidno_value" class="inptxt w160" value="" type="text" />
</td>
<td rowspan="1" colspan="1"><select id="pcountry_value" class="w160"><option value="CN"><span>中国CHINA</span>
</option>
<option value="US"><span>美国UNITEDSTATES</span>
</option>
<option value="AF"><span>阿富汗AFGHANISTANA</span>
</option>
<option value="AL"><span>阿尔巴尼亚ALBANIA</span>
</option>
<option value="DZ"><span>阿尔及利亚ALGERIA</span>
</option>
<option value="AD"><span>安道尔ANDORRA</span>
</option>
<option value="AO"><span>安哥拉ANGOLA</span>
</option>
<option value="AG"><span>安提瓜和巴布达ANTIGUABARBUDA</span>
</option>
<option value="AE"><span>阿拉伯联合酋长国ARAB</span>
</option>
<option value="AR"><span>阿根廷ARGENTINA</span>
</option>
<option value="AM"><span>亚美尼亚ARMENIA</span>
</option>
<option value="AW"><span>阿鲁巴ARUBA</span>
</option>
<option value="AU"><span>澳大利亚AUSTRALIA</span>
</option>
<option value="AT"><span>奥地利AUSTRIA</span>
</option>
<option value="AZ"><span>阿塞拜疆共和国AZERBAIJAN</span>
</option>
<option value="BS"><span>巴哈马BAHAMAS</span>
</option>
<option value="BH"><span>巴林BAHRAIN</span>
</option>
<option value="BD"><span>孟加拉国BANGLADESH</span>
</option>
<option value="BB"><span>巴巴多斯BARBADOS</span>
</option>
<option value="BY"><span>白俄罗斯BELARUS</span>
</option>
<option value="BE"><span>比利时BELGIUM</span>
</option>
<option value="BZ"><span>伯里兹BELIZE</span>
</option>
<option value="BZ"><span>伯利兹BELIZE</span>
</option>
<option value="BJ"><span>贝宁BENIN</span>
</option>
<option value="BT"><span>不丹BHUTAN</span>
</option>
<option value="BO"><span>玻利维亚BOLIVIA</span>
</option>
<option value="BA"><span>波斯尼亚和黑塞哥维那BOSNIA</span>
</option>
<option value="BW"><span>博茨瓦纳BOTSWANA</span>
</option>
<option value="BR"><span>巴西BRAZIL</span>
</option>
<option value="BG"><span>保加利亚BULGARIA</span>
</option>
<option value="BF"><span>布基纳法索BURKINAFASO</span>
</option>
<option value="BI"><span>布隆迪BURUNDI</span>
</option>
<option value="BN"><span>文莱BruneiDarussalam</span>
</option>
<option value="KH"><span>柬埔寨CAMBODIA</span>
</option>
<option value="CM"><span>喀麦隆CAMEROON</span>
</option>
<option value="CA"><span>加拿大CANADA</span>
</option>
<option value="KY"><span>佛得角CAPEVERDE</span>
</option>
<option value="TD"><span>乍得CHAD</span>
</option>
<option value="CL"><span>智利CHILE</span>
</option>
<option value="CO"><span>哥伦比亚COLOMBIA</span>
</option>
<option value="CO"><span>哥伦比亚COLUMBIA</span>
</option>
<option value="KM"><span>科摩罗COMOROS</span>
</option>
<option value="CG"><span>刚果（布）CONGO</span>
</option>
<option value="CK"><span>库克群岛COOKISLANDS</span>
</option>
<option value="CI"><span>科特迪瓦COTEDLVOIRE</span>
</option>
<option value="HR"><span>克罗地亚CROATIA</span>
</option>
<option value="CU"><span>古巴共和国CUBA</span>
</option>
<option value="CY"><span>塞浦路斯CYPRUS</span>
</option>
<option value="CZ"><span>捷克共和国CZECHREPUBLIC</span>
</option>
<option value="CF"><span>中非共和国Central Africa Republic</span>
</option>
<option value="CRC"><span>哥斯达黎加CostaRica</span>
</option>
<option value="CD"><span>刚果（金）DEMOCRATIC REPUBLIC OF CONGO</span>
</option>
<option value="YD"><span>也门民主人民共和国DEMOCRATICYEMEN</span>
</option>
<option value="DK"><span>丹麦DENMARK</span>
</option>
<option value="DJ"><span>吉布提DJIBOUTI</span>
</option>
<option value="DM"><span>多米尼克DOMINICA</span>
</option>
<option value="DO"><span>多米尼加DOMINICAN REPUBLIC</span>
</option>
<option value="EC"><span>厄瓜多尔ECUADOR</span>
</option>
<option value="EG"><span>埃及EGYPT</span>
</option>
<option value="EV"><span>萨尔瓦多EL SALVADOR</span>
</option>
<option value="GQ"><span>赤道几内亚EQUATORIALGUINEA</span>
</option>
<option value="ER"><span>厄立特里亚ERITREA</span>
</option>
<option value="EE"><span>爱沙尼亚ESTONIA</span>
</option>
<option value="ET"><span>埃塞俄比亚ETHIOPIA</span>
</option>
<option value="FJ"><span>斐济FIJI</span>
</option>
<option value="FI"><span>芬兰FINLAND</span>
</option>
<option value="FR"><span>法国FRANCE</span>
</option>
<option value="GA"><span>加蓬GABON</span>
</option>
<option value="GM"><span>冈比亚GAMBIA</span>
</option>
<option value="CE"><span>格鲁吉亚GEORGIA</span>
</option>
<option value="DE"><span>德国GERMANY</span>
</option>
<option value="GH"><span>加纳GHANA</span>
</option>
<option value="GR"><span>希腊GREECE</span>
</option>
<option value="GL"><span>格林纳达GRENADA</span>
</option>
<option value="GN"><span>几内亚GUINEA</span>
</option>
<option value="GW"><span>几内亚比绍GUINEA-BISSAU</span>
</option>
<option value="GW"><span>几内亚比绍GUINEABISSAU</span>
</option>
<option value="GY"><span>圭亚那GUYANA</span>
</option>
<option value="GT"><span>危地马拉Guatemala</span>
</option>
<option value="HT"><span>海地HAITI</span>
</option>
<option value="NL"><span>荷兰HOLLAND</span>
</option>
<option value="HN"><span>洪都拉斯HONDURAS</span>
</option>
<option value="HU"><span>匈牙利HUNGARY</span>
</option>
<option value="IS"><span>冰岛ICELAND</span>
</option>
<option value="IN"><span>印度INDIA</span>
</option>
<option value="ID"><span>印度尼西亚INDONESIA</span>
</option>
<option value="IR"><span>伊朗IRAN</span>
</option>
<option value="IQ"><span>伊拉克IRAQ</span>
</option>
<option value="IE"><span>爱尔兰IRELAND</span>
</option>
<option value="IL"><span>以色列ISRAEL</span>
</option>
<option value="IT"><span>意大利ITALY</span>
</option>
<option value="JM"><span>牙买加JAMAICA</span>
</option>
<option value="JP"><span>日本JAPAN</span>
</option>
<option value="JO"><span>约旦JORDAN</span>
</option>
<option value="KZ"><span>哈萨克斯坦KAZAKHSTAN</span>
</option>
<option value="KE"><span>肯尼亚KENYA</span>
</option>
<option value="KG"><span>吉尔吉斯共和国KIRGIZSTAN</span>
</option>
<option value="KI"><span>基里巴斯KIRIBATI</span>
</option>
<option value="KR"><span>韩国KOREA</span>
</option>
<option value="KW"><span>科威特KUWAIT</span>
</option>
<option value="DPR"><span>朝鲜Korea</span>
</option>
<option value="LA"><span>老挝LAOS</span>
</option>
<option value="LV"><span>拉脱维亚LATVIA</span>
</option>
<option value="LB"><span>黎巴嫩LEBANON</span>
</option>
<option value="LS"><span>莱索托LESOTHO</span>
</option>
<option value="LR"><span>利比里亚LIBERIA</span>
</option>
<option value="LY"><span>利比亚LIBYA</span>
</option>
<option value="LI"><span>列支敦士登LIECHTENSTEIN</span>
</option>
<option value="LT"><span>立陶宛LITHUANIA</span>
</option>
<option value="LU"><span>卢森堡LUXEMBOURG</span>
</option>
<option value="MK"><span>马其顿MACEDONIA</span>
</option>
<option value="MG"><span>马达加斯加MADAGASCAR</span>
</option>
<option value="MW"><span>马拉维MALAWI</span>
</option>
<option value="MY"><span>马来西亚MALAYSIA</span>
</option>
<option value="MV"><span>马尔代夫MALDIVES</span>
</option>
<option value="ML"><span>马里MALI</span>
</option>
<option value="MT"><span>马耳他MALTA</span>
</option>
<option value="MH"><span>马绍尔群岛MARSHALL ISLANDS</span>
</option>
<option value="MR"><span>毛里塔尼亚MAURITANIA</span>
</option>
<option value="MU"><span>毛里求斯MAURITIUS</span>
</option>
<option value="MX"><span>墨西哥MEXICO</span>
</option>
<option value="FM"><span>密克罗尼西亚联邦MICRONESIA</span>
</option>
<option value="MD"><span>摩尔多瓦MOLDOVA</span>
</option>
<option value="MC"><span>摩纳哥MONACO</span>
</option>
<option value="MN"><span>蒙古MONGOLIA</span>
</option>
<option value="ME"><span>黑山MONTENEGRO</span>
</option>
<option value="MA"><span>摩洛哥MOROCCO</span>
</option>
<option value="MZ"><span>莫桑比克MOZAMBIQUE</span>
</option>
<option value="MM"><span>缅甸MYANMAR</span>
</option>
<option value="NA"><span>纳米比亚NAMIBIA</span>
</option>
<option value="NR"><span>瑙鲁NAURU</span>
</option>
<option value="NP"><span>尼泊尔NEPAL</span>
</option>
<option value="NZ"><span>新西兰NEWZEALAND</span>
</option>
<option value="NI"><span>尼加拉瓜NICARAGUA</span>
</option>
<option value="NE"><span>尼日尔NIGER</span>
</option>
<option value="NG"><span>尼日利亚NIGERIA</span>
</option>
<option value="NO"><span>挪威NORWAY</span>
</option>
<option value="OM"><span>阿曼OMAN</span>
</option>
<option value="PK"><span>巴基斯坦PAKISTAN</span>
</option>
<option value="PW"><span>帕劳PALAU</span>
</option>
<option value="BL"><span>巴勒斯坦PALESTINE</span>
</option>
<option value="PA"><span>巴拿马PANAMA</span>
</option>
<option value="PG"><span>巴布亚新几内亚PAPUANEWGUINEA</span>
</option>
<option value="PY"><span>巴拉圭PARAGUAY</span>
</option>
<option value="PE"><span>秘鲁PERU</span>
</option>
<option value="PH"><span>菲律宾PHILIPPINES</span>
</option>
<option value="PL"><span>波兰POLAND</span>
</option>
<option value="PT"><span>葡萄牙PORTUGAL</span>
</option>
<option value="PR"><span>波多黎各PUERTO RICO</span>
</option>
<option value="QA"><span>卡塔尔QATAR</span>
</option>
<option value="RO"><span>罗马尼亚ROMANIA</span>
</option>
<option value="RU"><span>俄罗斯RUSSIA</span>
</option>
<option value="RW"><span>卢旺达RWANDA</span>
</option>
<option value="KNA"><span>圣基茨和尼维斯SAINT KITTS</span>
</option>
<option value="VC"><span>圣文森特和格林纳丁斯SAINT VINCENT AND THE GRENADIN</span>
</option>
<option value="LC"><span>圣卢西亚SAINTLUCIA</span>
</option>
<option value="WS"><span>美属萨摩亚SAMOA</span>
</option>
<option value="SM"><span>圣马力诺SANMARINO</span>
</option>
<option value="ST"><span>圣多美和普林西比SAOTOMEPRINCIPE</span>
</option>
<option value="SA"><span>沙特阿拉伯SAUDIARABIA</span>
</option>
<option value="SN"><span>塞内加尔SENEGAL</span>
</option>
<option value="CS"><span>塞尔维亚SERBIA</span>
</option>
<option value="SC"><span>塞舌尔SEYCHELLES</span>
</option>
<option value="SL"><span>塞拉利昂SIERRALEONE</span>
</option>
<option value="SG"><span>新加坡SINGAPORE</span>
</option>
<option value="SK"><span>斯洛伐克SLOVAKIA</span>
</option>
<option value="SK"><span>斯洛伐克共和国SLOVAKREPUBLIC</span>
</option>
<option value="SI"><span>斯洛文尼亚SLOVENIA</span>
</option>
<option value="SB"><span>所罗门群岛SOLOMON ISLANDS</span>
</option>
<option value="SO"><span>索马里SOMALI</span>
</option>
<option value="SO"><span>索马里SOMALIA</span>
</option>
<option value="ZA"><span>南非SOUTHAFRICA</span>
</option>
<option value="ES"><span>西班牙SPAIN</span>
</option>
<option value="LK"><span>斯里兰卡SRILANKA</span>
</option>
<option value="SD"><span>苏丹SUDAN</span>
</option>
<option value="SR"><span>苏里南SURINAM</span>
</option>
<option value="SZ"><span>斯威士兰SWAZILAND</span>
</option>
<option value="SE"><span>瑞典SWEDEN</span>
</option>
<option value="CH"><span>瑞士SWITZERLAND</span>
</option>
<option value="SY"><span>叙利亚SYRIA</span>
</option>
<option value="TJ"><span>塔吉克斯坦TAJIKISTAN</span>
</option>
<option value="TZ"><span>坦桑尼亚TANZANIA</span>
</option>
<option value="TH"><span>泰国THAILAND</span>
</option>
<option value="SS"><span>南苏丹共和国THE REPBLIC OF SOUTH SUDAN</span>
</option>
<option value="UGA"><span>乌干达THE REPUBLIC OF UGANDA</span>
</option>
<option value="TL"><span>东帝汶TIMOR</span>
</option>
<option value="TG"><span>多哥TOGO</span>
</option>
<option value="TO"><span>汤加TONGA</span>
</option>
<option value="TT"><span>特立尼达和多巴哥TRINIDADANDTOBAGO</span>
</option>
<option value="TN"><span>突尼斯TUNISIA</span>
</option>
<option value="TR"><span>土耳其TURKEY</span>
</option>
<option value="TM"><span>土库曼斯坦TURKMENISTAN</span>
</option>
<option value="UKR"><span>乌克兰UKRAINE</span>
</option>
<option value="GB"><span>英国UNITED KINGDOM</span>
</option>
<option value="UZB"><span>乌兹别克斯坦UZBEKISTAN</span>
</option>
<option value="UY"><span>乌拉圭Uruguay</span>
</option>
<option value="VU"><span>瓦努阿图VANUATU</span>
</option>
<option value="VA"><span>梵蒂冈VATICAN</span>
</option>
<option value="VIE"><span>越南VIETNAM</span>
</option>
<option value="VE"><span>委内瑞拉Venezuela</span>
</option>
<option value="ZM"><span>赞比亚ZAMBIA</span>
</option>
<option value="ZW"><span>津巴布韦ZIMBABWE</span>
</option>
</select>
</td>
</tr>
<tr id="error_tr" style="display: none;"><td colspan="5" rowspan="1"><span class="txt-wrong" id="error_for_nameandidno" style=""></span>
</td>
</tr>
</tbody>
</table>
<div class="lay-btn"><a href="javascript:" id="dialog_add_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="dialog_add_ok" class="btn92s" shape="rect">确认</a>
</div>
</div>
</div>
</div>
<div id="dialog_update" style="display: none;"><div class="mark"></div>
<div class="up-box" style="width:640px;"><div class="up-box-hd">修改乘客信息<a href="javascript:" id="dialog_update_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd" style="padding:15px 10px;border:1px solid #298CCE;"><table class="per-ticket" style="margin-left:0px;"><tr><th style="text-align:center;" rowspan="1" colspan="1">票种</th>
<th style="text-align:center;" rowspan="1" colspan="1">姓名</th>
<th style="text-align:center;" rowspan="1" colspan="1">证件类型</th>
<th style="text-align:center;" rowspan="1" colspan="1">证件号码</th>
<th style="text-align:center;" rowspan="1" colspan="1">国家/地区</th>
</tr>
<tbody id="showaddpassenger_update"><tr><td rowspan="1" colspan="1"><select id="ptypeselect_update"></select>
</td>
<td rowspan="1" colspan="1"><div><input id="pname_update_value" class="inptxt w110" type="text" />
</div>
</td>
<td rowspan="1" colspan="1"><select id="typeselect_update"></select>
</td>
<td rowspan="1" colspan="1"><input id="pidno_update_value" class="inptxt w160" value="" type="text" />
</td>
<td rowspan="1" colspan="1"><select id="pcountry_udpate_value" class="w160"><option value="CN"><span>中国CHINA</span>
</option>
<option value="US"><span>美国UNITEDSTATES</span>
</option>
<option value="AF"><span>阿富汗AFGHANISTANA</span>
</option>
<option value="AL"><span>阿尔巴尼亚ALBANIA</span>
</option>
<option value="DZ"><span>阿尔及利亚ALGERIA</span>
</option>
<option value="AD"><span>安道尔ANDORRA</span>
</option>
<option value="AO"><span>安哥拉ANGOLA</span>
</option>
<option value="AG"><span>安提瓜和巴布达ANTIGUABARBUDA</span>
</option>
<option value="AE"><span>阿拉伯联合酋长国ARAB</span>
</option>
<option value="AR"><span>阿根廷ARGENTINA</span>
</option>
<option value="AM"><span>亚美尼亚ARMENIA</span>
</option>
<option value="AW"><span>阿鲁巴ARUBA</span>
</option>
<option value="AU"><span>澳大利亚AUSTRALIA</span>
</option>
<option value="AT"><span>奥地利AUSTRIA</span>
</option>
<option value="AZ"><span>阿塞拜疆共和国AZERBAIJAN</span>
</option>
<option value="BS"><span>巴哈马BAHAMAS</span>
</option>
<option value="BH"><span>巴林BAHRAIN</span>
</option>
<option value="BD"><span>孟加拉国BANGLADESH</span>
</option>
<option value="BB"><span>巴巴多斯BARBADOS</span>
</option>
<option value="BY"><span>白俄罗斯BELARUS</span>
</option>
<option value="BE"><span>比利时BELGIUM</span>
</option>
<option value="BZ"><span>伯里兹BELIZE</span>
</option>
<option value="BZ"><span>伯利兹BELIZE</span>
</option>
<option value="BJ"><span>贝宁BENIN</span>
</option>
<option value="BT"><span>不丹BHUTAN</span>
</option>
<option value="BO"><span>玻利维亚BOLIVIA</span>
</option>
<option value="BA"><span>波斯尼亚和黑塞哥维那BOSNIA</span>
</option>
<option value="BW"><span>博茨瓦纳BOTSWANA</span>
</option>
<option value="BR"><span>巴西BRAZIL</span>
</option>
<option value="BG"><span>保加利亚BULGARIA</span>
</option>
<option value="BF"><span>布基纳法索BURKINAFASO</span>
</option>
<option value="BI"><span>布隆迪BURUNDI</span>
</option>
<option value="BN"><span>文莱BruneiDarussalam</span>
</option>
<option value="KH"><span>柬埔寨CAMBODIA</span>
</option>
<option value="CM"><span>喀麦隆CAMEROON</span>
</option>
<option value="CA"><span>加拿大CANADA</span>
</option>
<option value="KY"><span>佛得角CAPEVERDE</span>
</option>
<option value="TD"><span>乍得CHAD</span>
</option>
<option value="CL"><span>智利CHILE</span>
</option>
<option value="CO"><span>哥伦比亚COLOMBIA</span>
</option>
<option value="CO"><span>哥伦比亚COLUMBIA</span>
</option>
<option value="KM"><span>科摩罗COMOROS</span>
</option>
<option value="CG"><span>刚果（布）CONGO</span>
</option>
<option value="CK"><span>库克群岛COOKISLANDS</span>
</option>
<option value="CI"><span>科特迪瓦COTEDLVOIRE</span>
</option>
<option value="HR"><span>克罗地亚CROATIA</span>
</option>
<option value="CU"><span>古巴共和国CUBA</span>
</option>
<option value="CY"><span>塞浦路斯CYPRUS</span>
</option>
<option value="CZ"><span>捷克共和国CZECHREPUBLIC</span>
</option>
<option value="CF"><span>中非共和国Central Africa Republic</span>
</option>
<option value="CRC"><span>哥斯达黎加CostaRica</span>
</option>
<option value="CD"><span>刚果（金）DEMOCRATIC REPUBLIC OF CONGO</span>
</option>
<option value="YD"><span>也门民主人民共和国DEMOCRATICYEMEN</span>
</option>
<option value="DK"><span>丹麦DENMARK</span>
</option>
<option value="DJ"><span>吉布提DJIBOUTI</span>
</option>
<option value="DM"><span>多米尼克DOMINICA</span>
</option>
<option value="DO"><span>多米尼加DOMINICAN REPUBLIC</span>
</option>
<option value="EC"><span>厄瓜多尔ECUADOR</span>
</option>
<option value="EG"><span>埃及EGYPT</span>
</option>
<option value="EV"><span>萨尔瓦多EL SALVADOR</span>
</option>
<option value="GQ"><span>赤道几内亚EQUATORIALGUINEA</span>
</option>
<option value="ER"><span>厄立特里亚ERITREA</span>
</option>
<option value="EE"><span>爱沙尼亚ESTONIA</span>
</option>
<option value="ET"><span>埃塞俄比亚ETHIOPIA</span>
</option>
<option value="FJ"><span>斐济FIJI</span>
</option>
<option value="FI"><span>芬兰FINLAND</span>
</option>
<option value="FR"><span>法国FRANCE</span>
</option>
<option value="GA"><span>加蓬GABON</span>
</option>
<option value="GM"><span>冈比亚GAMBIA</span>
</option>
<option value="CE"><span>格鲁吉亚GEORGIA</span>
</option>
<option value="DE"><span>德国GERMANY</span>
</option>
<option value="GH"><span>加纳GHANA</span>
</option>
<option value="GR"><span>希腊GREECE</span>
</option>
<option value="GL"><span>格林纳达GRENADA</span>
</option>
<option value="GN"><span>几内亚GUINEA</span>
</option>
<option value="GW"><span>几内亚比绍GUINEA-BISSAU</span>
</option>
<option value="GW"><span>几内亚比绍GUINEABISSAU</span>
</option>
<option value="GY"><span>圭亚那GUYANA</span>
</option>
<option value="GT"><span>危地马拉Guatemala</span>
</option>
<option value="HT"><span>海地HAITI</span>
</option>
<option value="NL"><span>荷兰HOLLAND</span>
</option>
<option value="HN"><span>洪都拉斯HONDURAS</span>
</option>
<option value="HU"><span>匈牙利HUNGARY</span>
</option>
<option value="IS"><span>冰岛ICELAND</span>
</option>
<option value="IN"><span>印度INDIA</span>
</option>
<option value="ID"><span>印度尼西亚INDONESIA</span>
</option>
<option value="IR"><span>伊朗IRAN</span>
</option>
<option value="IQ"><span>伊拉克IRAQ</span>
</option>
<option value="IE"><span>爱尔兰IRELAND</span>
</option>
<option value="IL"><span>以色列ISRAEL</span>
</option>
<option value="IT"><span>意大利ITALY</span>
</option>
<option value="JM"><span>牙买加JAMAICA</span>
</option>
<option value="JP"><span>日本JAPAN</span>
</option>
<option value="JO"><span>约旦JORDAN</span>
</option>
<option value="KZ"><span>哈萨克斯坦KAZAKHSTAN</span>
</option>
<option value="KE"><span>肯尼亚KENYA</span>
</option>
<option value="KG"><span>吉尔吉斯共和国KIRGIZSTAN</span>
</option>
<option value="KI"><span>基里巴斯KIRIBATI</span>
</option>
<option value="KR"><span>韩国KOREA</span>
</option>
<option value="KW"><span>科威特KUWAIT</span>
</option>
<option value="DPR"><span>朝鲜Korea</span>
</option>
<option value="LA"><span>老挝LAOS</span>
</option>
<option value="LV"><span>拉脱维亚LATVIA</span>
</option>
<option value="LB"><span>黎巴嫩LEBANON</span>
</option>
<option value="LS"><span>莱索托LESOTHO</span>
</option>
<option value="LR"><span>利比里亚LIBERIA</span>
</option>
<option value="LY"><span>利比亚LIBYA</span>
</option>
<option value="LI"><span>列支敦士登LIECHTENSTEIN</span>
</option>
<option value="LT"><span>立陶宛LITHUANIA</span>
</option>
<option value="LU"><span>卢森堡LUXEMBOURG</span>
</option>
<option value="MK"><span>马其顿MACEDONIA</span>
</option>
<option value="MG"><span>马达加斯加MADAGASCAR</span>
</option>
<option value="MW"><span>马拉维MALAWI</span>
</option>
<option value="MY"><span>马来西亚MALAYSIA</span>
</option>
<option value="MV"><span>马尔代夫MALDIVES</span>
</option>
<option value="ML"><span>马里MALI</span>
</option>
<option value="MT"><span>马耳他MALTA</span>
</option>
<option value="MH"><span>马绍尔群岛MARSHALL ISLANDS</span>
</option>
<option value="MR"><span>毛里塔尼亚MAURITANIA</span>
</option>
<option value="MU"><span>毛里求斯MAURITIUS</span>
</option>
<option value="MX"><span>墨西哥MEXICO</span>
</option>
<option value="FM"><span>密克罗尼西亚联邦MICRONESIA</span>
</option>
<option value="MD"><span>摩尔多瓦MOLDOVA</span>
</option>
<option value="MC"><span>摩纳哥MONACO</span>
</option>
<option value="MN"><span>蒙古MONGOLIA</span>
</option>
<option value="ME"><span>黑山MONTENEGRO</span>
</option>
<option value="MA"><span>摩洛哥MOROCCO</span>
</option>
<option value="MZ"><span>莫桑比克MOZAMBIQUE</span>
</option>
<option value="MM"><span>缅甸MYANMAR</span>
</option>
<option value="NA"><span>纳米比亚NAMIBIA</span>
</option>
<option value="NR"><span>瑙鲁NAURU</span>
</option>
<option value="NP"><span>尼泊尔NEPAL</span>
</option>
<option value="NZ"><span>新西兰NEWZEALAND</span>
</option>
<option value="NI"><span>尼加拉瓜NICARAGUA</span>
</option>
<option value="NE"><span>尼日尔NIGER</span>
</option>
<option value="NG"><span>尼日利亚NIGERIA</span>
</option>
<option value="NO"><span>挪威NORWAY</span>
</option>
<option value="OM"><span>阿曼OMAN</span>
</option>
<option value="PK"><span>巴基斯坦PAKISTAN</span>
</option>
<option value="PW"><span>帕劳PALAU</span>
</option>
<option value="BL"><span>巴勒斯坦PALESTINE</span>
</option>
<option value="PA"><span>巴拿马PANAMA</span>
</option>
<option value="PG"><span>巴布亚新几内亚PAPUANEWGUINEA</span>
</option>
<option value="PY"><span>巴拉圭PARAGUAY</span>
</option>
<option value="PE"><span>秘鲁PERU</span>
</option>
<option value="PH"><span>菲律宾PHILIPPINES</span>
</option>
<option value="PL"><span>波兰POLAND</span>
</option>
<option value="PT"><span>葡萄牙PORTUGAL</span>
</option>
<option value="PR"><span>波多黎各PUERTO RICO</span>
</option>
<option value="QA"><span>卡塔尔QATAR</span>
</option>
<option value="RO"><span>罗马尼亚ROMANIA</span>
</option>
<option value="RU"><span>俄罗斯RUSSIA</span>
</option>
<option value="RW"><span>卢旺达RWANDA</span>
</option>
<option value="KNA"><span>圣基茨和尼维斯SAINT KITTS</span>
</option>
<option value="VC"><span>圣文森特和格林纳丁斯SAINT VINCENT AND THE GRENADIN</span>
</option>
<option value="LC"><span>圣卢西亚SAINTLUCIA</span>
</option>
<option value="WS"><span>美属萨摩亚SAMOA</span>
</option>
<option value="SM"><span>圣马力诺SANMARINO</span>
</option>
<option value="ST"><span>圣多美和普林西比SAOTOMEPRINCIPE</span>
</option>
<option value="SA"><span>沙特阿拉伯SAUDIARABIA</span>
</option>
<option value="SN"><span>塞内加尔SENEGAL</span>
</option>
<option value="CS"><span>塞尔维亚SERBIA</span>
</option>
<option value="SC"><span>塞舌尔SEYCHELLES</span>
</option>
<option value="SL"><span>塞拉利昂SIERRALEONE</span>
</option>
<option value="SG"><span>新加坡SINGAPORE</span>
</option>
<option value="SK"><span>斯洛伐克SLOVAKIA</span>
</option>
<option value="SK"><span>斯洛伐克共和国SLOVAKREPUBLIC</span>
</option>
<option value="SI"><span>斯洛文尼亚SLOVENIA</span>
</option>
<option value="SB"><span>所罗门群岛SOLOMON ISLANDS</span>
</option>
<option value="SO"><span>索马里SOMALI</span>
</option>
<option value="SO"><span>索马里SOMALIA</span>
</option>
<option value="ZA"><span>南非SOUTHAFRICA</span>
</option>
<option value="ES"><span>西班牙SPAIN</span>
</option>
<option value="LK"><span>斯里兰卡SRILANKA</span>
</option>
<option value="SD"><span>苏丹SUDAN</span>
</option>
<option value="SR"><span>苏里南SURINAM</span>
</option>
<option value="SZ"><span>斯威士兰SWAZILAND</span>
</option>
<option value="SE"><span>瑞典SWEDEN</span>
</option>
<option value="CH"><span>瑞士SWITZERLAND</span>
</option>
<option value="SY"><span>叙利亚SYRIA</span>
</option>
<option value="TJ"><span>塔吉克斯坦TAJIKISTAN</span>
</option>
<option value="TZ"><span>坦桑尼亚TANZANIA</span>
</option>
<option value="TH"><span>泰国THAILAND</span>
</option>
<option value="SS"><span>南苏丹共和国THE REPBLIC OF SOUTH SUDAN</span>
</option>
<option value="UGA"><span>乌干达THE REPUBLIC OF UGANDA</span>
</option>
<option value="TL"><span>东帝汶TIMOR</span>
</option>
<option value="TG"><span>多哥TOGO</span>
</option>
<option value="TO"><span>汤加TONGA</span>
</option>
<option value="TT"><span>特立尼达和多巴哥TRINIDADANDTOBAGO</span>
</option>
<option value="TN"><span>突尼斯TUNISIA</span>
</option>
<option value="TR"><span>土耳其TURKEY</span>
</option>
<option value="TM"><span>土库曼斯坦TURKMENISTAN</span>
</option>
<option value="UKR"><span>乌克兰UKRAINE</span>
</option>
<option value="GB"><span>英国UNITED KINGDOM</span>
</option>
<option value="UZB"><span>乌兹别克斯坦UZBEKISTAN</span>
</option>
<option value="UY"><span>乌拉圭Uruguay</span>
</option>
<option value="VU"><span>瓦努阿图VANUATU</span>
</option>
<option value="VA"><span>梵蒂冈VATICAN</span>
</option>
<option value="VIE"><span>越南VIETNAM</span>
</option>
<option value="VE"><span>委内瑞拉Venezuela</span>
</option>
<option value="ZM"><span>赞比亚ZAMBIA</span>
</option>
<option value="ZW"><span>津巴布韦ZIMBABWE</span>
</option>
</select>
</td>
</tr>
<tr id="error_update_tr" style="display: none;"><td colspan="5" rowspan="1"><span class="txt-wrong" id="error_for_update_nameandidno" style=""></span>
</td>
</tr>
</tbody>
</table>
<div class="lay-btn"><a href="javascript:" id="dialog_update_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="dialog_update_ok" class="btn92s" shape="rect">确认</a>
</div>
</div>
</div>
</div>
<div id="608_complain" style="display: none;"><div class="mark"></div>
<div class="up-box" style="width:640px;"><div class="up-box-hd">举报告知确认书<a href="javascript:" id="608_complain_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd" style="padding:15px 10px;border:1px solid #298CCE;"><table class="per-ticket" style="margin-left:0px;"><tr><td rowspan="1" colspan="1">举报人姓名：<strong id="608_name" style="font-size:20px"></strong>
</td>
<td rowspan="1" colspan="1">联系电话：<strong id="608_tel" style="font-size:20px"></strong>
</td>
</tr>
<tr><td colspan="2" rowspan="1">身份证件号码：<strong id="608_card" style="font-size:20px"></strong>
</td>
</tr>
<tr></tr>
<tr><td colspan="2" rowspan="1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人确认举报身份信息被他人冒用购买<strong id="ticketInfo" style="font-size:20px"></strong>
次车票。本人承诺本次举报及购票所提交的身份信息属实，并对虚假举报后果负责。</td>
</tr>
<tr><td colspan="2" rowspan="1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;铁路部门郑重提醒，将在车站和列车对该车票进行重点查验。根据国务院颁布的《铁路安全管理条例》，对该车票所记载身份信息与所持身份证件或者真实身份不符的持票人，铁路部门将拒绝其进站乘车。同时，公安机关将依法调查。</td>
</tr>
<tr><td colspan="2" rowspan="1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;铁路部门将对您的举报信息保密，谢谢您的合作！</td>
</tr>
</table>
<div class="lay-btn"><a href="javascript:" id="608_complain_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="608_complain_ok" class="btn92s" shape="rect">确认举报</a>
</div>
</div>
</div>
</div>
<div id="608_check" style="display: none;"><div class="mark"></div>
<div class="up-box"><div class="up-box-hd">温馨提示<a href="javascript:" id="608_check_close" shape="rect">关闭</a>
</div>
<div class="up-box-bd"><div class="up-con clearfix"><span class="icon i-opt"></span>
<div class="r-txt"><div class="tit" id="608_check_msg"></div>
<div class="tit" style="color:#FB7403">是否举报？</div>
</div>
</div>
<div class="lay-btn"><a href="javascript:" id="608_check_cancel" class="btn92" shape="rect">取消</a>
<a href="javascript:" id="608_check_ok" class="btn92s" shape="rect">网上举报</a>
</div>
</div>
</div>
</div>
<!--header start-->
<div class="header"><div class="wrapper"><!-- 头部内容 -->
<div class="header-con"><h1 class="logo"><a name="g_href" data-type="1" data-href="index.html" data-redirect="Y" href="javascript:;">中国铁路12306</a>
</h1>
<div class="header-right"><!-- 搜索条 -->
<div class="header-search"><div class="search-bd"><input type="password" value="" style="display:none" />
<input type="text" class="search-input" id="search-input" value="" auto-complete="new-password" placeholder="搜索车票/餐饮/常旅客/相关规章" />
<!-- 搜索提示 -->
<div class="search-down"><a href="javascript:;" class="close">关闭</a>
<ul class="search-down-list"></ul>
<!-- 热门推荐 -->
<!-- <div class="search-down-hot">
                            <h3 class="search-hot-tit">热门推荐</h3>
                            <div class="search-hot-key"><a href="#">车站</a><a href="#">进站乘车</a><a href="#">互联网购票</a></div>
                        </div> -->
</div>
<!-- 搜索历史 -->
<div class="search-history"><a href="javascript:;" class="history-clear">清除</a>
<h3 class="search-history-tit">搜索历史</h3>
<ul class="search-history-list"></ul>
</div>
</div>
<a class="search-btn" href="javascript:;"><i class="icon icon-search"></i>
</a>
</div>
<!-- 右侧菜单 -->
<ul class="header-menu"><li class="menu-item menu-nav"><a name="g_href" data-type="2" data-href="view/index.html" data-redirect="Y" href="javascript:;" class="menu-nav-hd">我的12306
                            <i class="caret"></i>
</a>
<ul class="menu-nav-bd"><li><a style="color: #333;" name="g_href" data-type="2" data-href="view/train_order.html" data-redirect="Y" href="javascript:;">火车票订单</a>
</li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/lineUp_order.html" data-redirect="Y" href="javascript:;">候补订单</a>
</li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/personal_travel.html" data-redirect="Y" href="javascript:;">我的行程</a>
</li>
<li class="nav-line"></li>
<li><a style="color: #333;" name="g_href" data-type="10" data-href="queryMyOrder.html" data-redirect="Y" href="javascript:;">我的餐饮•特产</a>
</li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/my_insurance.html" data-redirect="Y" href="javascript:;">我的保险</a>
</li>
<li><a style="color: #333;" name="g_href" data-type="3" data-href="welcome.html" data-redirect="Y" href="javascript:;">我的会员</a>
</li>
<li class="nav-line"></li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/information.html" data-redirect="Y" href="javascript:;">查看个人信息</a>
</li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/userSecurity.html" data-redirect="Y" href="javascript:;">账户安全</a>
</li>
<li class="nav-line"></li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/passengers.html" data-redirect="Y" href="javascript:;">常用联系人</a>
</li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/address_init.html" data-redirect="Y" href="javascript:;">车票快递地址</a>
</li>
<li class="nav-line"></li>
<li><a style="color: #333;" name="g_href" data-type="2" data-href="view/icentre_serviceQuery.html" data-redirect="Y" href="javascript:;">温馨服务查询</a>
</li>
</ul>
</li>
<li class="menu-item menu-line">|</li>
<li id="J-header-logout" class="menu-item menu-login">
                        您好，<a id="login_user" name="g_href" data-type="2" data-href="view/index.html" data-redirect="Y" href="javascript:;" class="colorA" style="margin-left:-0.5px;"><span style="width:50px;">加金安</span>
</a>
<span class="txt-primary"></span>
&nbsp;|&nbsp;<a name="g_href" data-type="2" data-href="login/loginOut" data-redirect="Y" href="javascript:;">退出</a>
</li>
</ul>
</div>
</div>
</div>
<!-- 导航 -->
<div class="nav-box"><ul class="nav"><li class="nav-item nav-item-w1"><a name="g_href" data-type="1" data-href="index.html" data-redirect="Y" href="javascript:;" class="nav-hd">首页</a>
</li>
<li class="nav-item nav-item-w1"><a href="javascript:void(0)" class="nav-hd">车票
                    <i class="icon icon-down"></i>
</a>
<div class="nav-bd"><div class="nav-bd-item nav-col2"><h3 class="nav-tit">购买</h3>
<ul class="nav-con"><li><a name="g_href" data-type="2" data-href="leftTicket/init?linktypeid=dc" data-redirect="Y" href="javascript:;">单程</a>
</li>
<li><a name="g_href" data-type="2" data-href="leftTicket/init?linktypeid=wf" data-redirect="Y" href="javascript:;">往返</a>
</li>
<li><a name="g_href" data-type="2" data-href="lcQuery/init" data-redirect="Y" href="javascript:;">接续换乘</a>
</li>
<li></li>
</ul>
</div>
<div class="nav-bd-item nav-col2"><h3 class="nav-tit">变更</h3>
<ul class="nav-con"><li><a name="g_href" data-type="2" data-href="view/train_order.html?type=2" data-param="typefilt=4" data-redirect="Y" href="javascript:;">退票</a>
</li>
<li><a name="g_href" data-type="2" data-href="view/train_order.html?type=2" data-param="typefilt=2" data-redirect="Y" href="javascript:;">改签</a>
</li>
<li><a name="g_href" data-type="2" data-href="view/train_order.html?type=2" data-param="typefilt=3" data-redirect="Y" href="javascript:;">变更到站</a>
</li>
<li></li>
</ul>
</div>
<div class="nav-bd-item nav-col2"><h3 class="nav-tit border-none">更多</h3>
<ul class="nav-con"><li><a name="g_href" data-type="1" data-href="view/ticket/zt_card.html" data-redirect="Y" href="javascript:;">中铁银通卡</a>
</li>
<li class="border-none"><a name="g_href" data-type="1" data-href="view/ticket/through_train.html" data-redirect="Y" href="javascript:;">广九直通车</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/ticket/railway.html" data-redirect="Y" href="javascript:;">市郊快速铁路</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/ticket/international_train.html" data-redirect="Y" href="javascript:;">国际列车</a>
</li>
</ul>
</div>
</div>
</li>
<li class="nav-item "><a href="javascript:void(0)" class="nav-hd ">团购服务
                    <i class="icon icon-down "></i>
</a>
<div class="nav-bd "><div class="nav-bd-item nav-col6 "><ul class="nav-con "><li><a name="g_href" data-type="1" data-href="view/group/group_management.html?type=1" data-redirect="Y" href="javascript:;">务工人员</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/group/group_management.html?type=2" data-redirect="Y" href="javascript:;">学生团体</a>
</li>
</ul>
</div>
</div>
</li>
<li class="nav-item "><a href="javascript:void(0) " class="nav-hd ">会员服务
                    <i class="icon icon-down "></i>
</a>
<div class="nav-bd "><div class="nav-bd-item nav-col6"><ul class="nav-con "><li><a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">会员管理</a>
</li>
<li><a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">积分账户</a>
</li>
<li><a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">积分兑换</a>
</li>
<li><a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">会员专享</a>
</li>
<li class="border-none "><a name="g_href" data-type="3" data-href="welcome.html" data-redirect="Y" href="javascript:;">会员中心</a>
</li>
</ul>
</div>
</div>
</li>
<li class="nav-item "><a href="javascript:void(0) " class="nav-hd ">站车服务
                    <i class="icon icon-down "></i>
</a>
<div class="nav-bd "><div class="nav-bd-item nav-col4 "><ul class="nav-con "><li><a name="g_href" data-type="2" data-href="view/icentre_qxyyInfo.html" data-redirect="Y" href="javascript:;">重点旅客预约</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/station/hand.html" data-redirect="Y" href="javascript:;">便民托运</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/station/shared_Car.html" data-redirect="Y" href="javascript:;">共享汽车</a>
</li>
<li><a name="g_href" data-type="4" data-href="czyd_2143/" data-redirect="Y" href="javascript:;">车站引导</a>
</li>
<li><a name="g_href" data-type="2" data-href="view/icentre_lostInfo.html" data-redirect="Y" href="javascript:;">遗失物品查找</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/station/train_intro.html" data-redirect="Y" href="javascript:;">动车组介绍</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/station/custom_PickUp.html" data-redirect="Y" href="javascript:;">定制接送</a>
</li>
<li><a name="g_href" data-type="4" data-href="zcfc_2548/" data-redirect="Y" href="javascript:;">站车风采</a>
</li>
</ul>
</div>
</div>
</li>
<li class="nav-item "><a href="javascript:void(0) " class="nav-hd ">商旅服务
                    <i class="icon icon-down "></i>
</a>
<div class="nav-bd "><div class="nav-bd-item nav-col6 "><ul class="nav-con "><li><a name="g_href" data-type="10" data-href="index.html" data-redirect="Y" href="javascript:;">餐饮•特产</a>
</li>
<li><a name="g_href" data-type="5" data-href="" data-redirect="Y" href="javascript:;">旅游</a>
</li>
<li><a name="g_href" data-type="2" data-href="view/my_insurance.html" data-redirect="Y" href="javascript:;">保险</a>
</li>
</ul>
</div>
</div>
</li>
<li class="nav-item "><a href="javascript:void(0) " class="nav-hd ">出行指南
                    <i class="icon icon-down "></i>
</a>
<div class="nav-bd "><div class="nav-bd-item nav-col2 "><h3 class="nav-tit ">常见问题</h3>
<ul class="nav-con "><li><a name="g_href" data-type="2" data-href="gonggao/ticketType.html" data-redirect="Y" href="javascript:;">车票</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/ticketWindow.html" data-redirect="Y" href="javascript:;">购票</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/windowEndorse.html" data-redirect="Y" href="javascript:;">改签、变更到站</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/windowRefund.html" data-redirect="Y" href="javascript:;">退票</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/help.html" data-redirect="Y" href="javascript:;" class="txt-lighter">更多>></a>
</li>
<li></li>
</ul>
</div>
<div class="nav-bd-item nav-col2 "><h3 class="nav-tit ">旅客须知</h3>
<ul class="nav-con "><li><a name="g_href" data-type="2" data-href="gonggao/usersNeedToKnow.html?linktypeid=txt" data-redirect="Y" href="javascript:;">铁路电子客票</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means5" data-redirect="Y" href="javascript:;">身份核验</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/help.html" data-redirect="Y" href="javascript:;" class="txt-lighter">更多>></a>
</li>
<li></li>
</ul>
</div>
<div class="nav-bd-item nav-col2 "><h3 class="nav-tit border-none ">相关章程</h3>
<ul class="nav-con "><li><a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means1" data-redirect="Y" href="javascript:;">铁路互联网售票暂行办法</a>
</li>
<li class="border-none "><a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means2" data-redirect="Y" href="javascript:;">铁路旅客运输规程</a>
</li>
<li style="text-overflow: ellipsis;white-space: nowrap;"><a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means6" data-redirect="Y" href="javascript:;">铁路进站乘车禁止和限制携带品公告</a>
</li>
<li class="border-none" style="text-overflow: ellipsis;white-space: nowrap;"><a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means7" data-redirect="Y" href="javascript:;">广深港高速铁路跨境旅客运输组织规则</a>
</li>
<li><a name="g_href" data-type="2" data-href="gonggao/help.html" data-redirect="Y" href="javascript:;" class="txt-lighter">更多>></a>
</li>
<li></li>
</ul>
</div>
</div>
</li>
<li class="nav-item last "><a href="javascript:void(0) " class="nav-hd ">信息查询
                    <i class="icon icon-down "></i>
</a>
<div class="nav-bd "><div class="nav-bd-item nav-col5 "><h3 class="nav-tit border-none ">常用查询</h3>
<ul class="nav-con "><li><a name="g_href" data-type="2" data-href="zwdch/init" data-redirect="Y" href="javascript:;">正晚点</a>
</li>
<li><a name="g_href" data-type="2" data-href="queryTrainInfo/init" data-redirect="Y" href="javascript:;">时刻表</a>
</li>
<li><a name="g_href" data-type="2" data-href="leftTicketPrice/initPublicPrice" data-redirect="Y" href="javascript:;">公布票价</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/infos/ticket_check.html" data-redirect="Y" href="javascript:;">检票口</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/infos/sale_time.html" data-redirect="Y" href="javascript:;">起售时间</a>
</li>
<li><a name="g_href" data-href="https://forecast.lytq.com/pc.html" data-redirect="N" href="javascript:;">天气</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/infos/jiaotong.html" data-redirect="Y" href="javascript:;">交通查询</a>
</li>
<li><a name="g_href" data-type="2" data-href="queryAgencySellTicket/init" data-redirect="Y" href="javascript:;">代售点</a>
</li>
<li><a name="g_href" data-type="1" data-href="view/infos/service_number.html" data-redirect="Y" href="javascript:;">客服电话</a>
</li>
<li></li>
</ul>
</div>
<div class="nav-bd-item "><ul class="nav-con nav-con-pt"><li class="border-none"><a name="g_href" data-type="1" data-href="index.html#index_ads" data-redirect="Y" href="javascript:;">最新发布</a>
</li>
<li class="border-none"><a name="g_href" data-type="6" data-href="queryDishonest/init" data-redirect="Y" href="javascript:;">信用信息</a>
</li>
</ul>
</div>
</div>
</li>
</ul>
</div>
</div>
<!--header end-->
<!--页面主体  开始-->
<div class="content"><!--列车信息 开始-->
<div class="layout t-info"><div class="lay-hd">
				列车信息<span class="small">（以下余票信息仅供参考）</span>
</div>
<div class="lay-bd"><p class="t-tit" id="ticket_tit_id"></p>
<p class="t-con" id="ticket_con_id"></p>
<p style="color: #3177BF;">
					*显示的卧铺票价均为上铺票价，供您参考。具体票价以您确认支付时实际购买的铺别票价为准。
				</p>
</div>
</div>
<!--列车信息 结束-->
<!--改签原票信息 开始-->
<!--改签原票信息 结束-->
<!--多级票价信息 开始-->
<div style="display: none;"><input style="display: none;" type="checkbox" id="fczk" />
</div>
<!--乘客信息 开始-->
<div class="layout person"><div class="lay-hd">
				乘客信息<span class="small" id="psInfo">（填写说明）</span>
<div class="s-box"><input id="quickQueryPassenger_id" type="text" value="输入乘客姓名" class="txt" />
<input id="submit_quickQueryPassenger" type="submit" class="sub" />
</div>
</div>
<div class="lay-bd"><div class="per-sel"><div class="item clearfix"><h2 class="srr" id="dg_passenger_image_id" title="受让人" style="display: none;">受让人</h2>
<ul id="dj_passenger_id"></ul>
</div>
<div class="item clearfix"><h2 class="cy" id="normal_passenger_image_id" title="常用联系人" style="display: none;">常用联系人</h2>
<ul id="normal_passenger_id"></ul>
<div class="btn-all" style="display: none;" id="btnAll"><a id="show_more_passenger_id" title="展开" href="javascript:" style="display: none;" shape="rect"><label id="gd">更多</label>
<b></b>
</a>
</div>
</div>
</div>
<table class="per-ticket"><tr><th width="28" rowspan="1" colspan="1">序号</th>
<th rowspan="1" colspan="1">票种</th>
<th rowspan="1" colspan="1">席别 </th>
<th rowspan="1" colspan="1">姓名</th>
<th rowspan="1" colspan="1">证件类型</th>
<th rowspan="1" colspan="1">证件号码</th>
<th rowspan="1" colspan="1">手机号码</th>
<!-- 
						<th><input type="checkbox" class="check" id="selected_ticket_passenger_all"
							onclick="javascript:selectedTicketPassengerAll(this,true);" checked="checked" />全部</th>
						-->
<th width="70" rowspan="1" colspan="1"></th>
<th width="30" rowspan="1" colspan="1"></th>
</tr>
<tbody id="ticketInfo_id"></tbody>
</table>
<div><img src="/otn/resources/images/ins_ad4.png" alt="" />
</div>
</div>
</div>
<!-- 
		//inside: class="lay-btn captchaButton passengerInfo-inside"
		//float: class="lay-btn captchaButton captchaFloatButton passengerInfo-float"
		 -->
<!--乘客信息 结束-->
<div class="lay-btn"><a id="preStep_id" href="javascript:" class="btn92" shape="rect">上一步</a>
<a id="submitOrder_id" href="javascript:" class="btn92s" shape="rect">提交订单</a>
</div>
<div class="lay-btn captchaButton passengerInfo-inside" data-touclick-name=""></div>
<div class="tips-txt"><h2>温馨提示：</h2>
<P>1. 一张有效身份证件同一乘车日期同一车次只能购买一张车票，高铁动卧列车除外。</P>
<P>2. 购票时可使用的有效身份证件包括：中华人民共和国居民身份证、港澳居民来往内地通行证、台湾居民来往大陆通行证和按规定可使用的有效护照。</P>
<P>3. 购买儿童票时，乘车儿童有有效身份证件的，请填写本人有效身份证件信息。乘车儿童没有有效身份证件的，应使用同行成年人的有效身份证件信息；购票时不受第一条限制，但购票后、开车前须办理换票手续方可进站乘车。</P>
<P>
				4. 购买学生票时，须在<a href="../view/passengers.html" shape="rect">我的常用联系人</a>
中登记乘车人的学生详细信息。学生票乘车时间限为每年的暑假6月1日至9月30日、寒假12月1日至3月31日。购票后、开车前，须办理换票手续方可进站乘车。换票时，新生凭录取通知书，毕业生凭学校书面证明，其他凭学生优惠卡。

			</P>
<P>5.
				购买残疾军人（伤残警察）优待票的，须在购票后、开车前办理换票手续方可进站乘车。换票时，不符合规定的减价优待条件，没有有效"中华人民共和国残疾军人证"或"中华人民共和国伤残人民警察证"的，不予换票，所购车票按规定办理退票手续。</P>
<P><strong>6.购买铁路乘意险的注册用户年龄须在18周岁以上，使用非中国居民身份证注册的用户如购买铁路乘意险，须在<a href="../view/information.html" shape="rect">我的12306——个人信息</a>
如实填写“出生日期”。</strong>
</P>
<P><strong>7.父母为未成年子女投保，须在<a href="../view/passengers.html" shape="rect">我的常用联系人</a>
登记未成年子女的有效身份证件信息。</strong>
</P>
<P>8.未尽事宜详见《铁路旅客运输规程》等有关规定和车站公告。</P>
</div>
</div>
<!--页面主体  结束-->
<!--页面底部  开始-->
<div class="footer"><div class="footer-con wrapper"><div class="foot-links" style="margin-right:20px;"><h2 class="foot-con-tit">友情链接</h2>
<ul class="foot-links-list"><li><a name="g_href" data-href="http://www.china-railway.com.cn/" data-redirect="N" href="javascript:;" data-target="_blank"><img src="/otn/resources/images/12306_index/link05.png" alt="" />
</a>
</li>
<li><a name="g_href" data-href="http://www.china-ric.com/" data-redirect="N" href="javascript:;" data-target="_blank"><img src="/otn/resources/images/12306_index/link02.png" alt="" />
</a>
</li>
<li><a name="g_href" data-href="http://www.95306.cn/" data-redirect="N" href="javascript:;" data-target="_blank"><img src="/otn/resources/images/12306_index/link03.png" alt="" />
</a>
</li>
<li><a name="g_href" data-href="http://www.cre.cn/" data-redirect="N" href="javascript:;" data-target="_blank"><img src="/otn/resources/images/12306_index/link04.png" alt="" />
</a>
</li>
</ul>
</div>
<ul class="foot-code"><li style="width: 140px;"><h2 class="foot-con-tit">中国铁路官方微信</h2>
<div class="code-pic"><img src="/otn/resources/images/zgtlwb.png" class="code-pic" alt="" />
</div>
</li>
<li style="width: 140px;"><h2 class="foot-con-tit">中国铁路官方微博</h2>
<div class="code-pic"><img src="/otn/resources/images/zgtlwx.png" class="code-pic" alt="" />
</div>
</li>
<li style="width: 110px;"><h2 class="foot-con-tit">12306 公众号</h2>
<div class="code-pic"><img src="/otn/resources/images/public.png" class="code-pic" alt="" />
</div>
</li>
<li style="width: 110px;"><h2 class="foot-con-tit">铁路12306</h2>
<div class="code-pic"><img src="/otn/resources/images/download.png" class="code-pic" alt="" />
<div class="code-tips">官方APP下载，目前铁路未授权其他网站或APP开展类似服务内容，敬请广大用户注意。</div>
</div>
</li>
</ul>
</div>
<div class="footer-txt"><p><span class="mr">版权所有©2008-2019</span>
<span>中国铁道科学研究院集团有限公司</span>
</p>
<p><span class="mr">京ICP备05020493号-4</span>
<span class="mr">|</span>
<span>京ICP证150437号</span>
</p>
</div>
</div>
<!--页面底部  结束-->
<!-- 提交订单核对车票信息弹出层 start -->
<div id="checkticketinfo_id" style="display: none; margin-left: 30%; margin-top: 30%;"><div class="mark"></div>
<div class="up-box w664" id="content_checkticketinfo_id"><div class="up-box-hd"><!-- <a id="close_checkticketdialog_id" href="javascript:">关闭</a> -->


				请核对以下信息

				

			</div>
<div class="up-box-bd ticket-check"><div class="info2" id="check_ticket_tit_id"><strong class="mr5">2013-03-02（周日）</strong>
<strong class="mr5">D315</strong>
动车<strong class="ml5">北京南</strong>
站<strong>（08:22开）—上海虹桥</strong>
站（16:55到）

				</div>
<table class="table-a"><tr><th width="28" rowspan="1" colspan="1">序号</th>
<th rowspan="1" colspan="1">席别</th>
<th id="bed_show" style="display: none;" rowspan="1" colspan="1">铺别</th>
<th rowspan="1" colspan="1">票种</th>
<th rowspan="1" colspan="1">姓名</th>
<th rowspan="1" colspan="1">证件类型</th>
<th rowspan="1" colspan="1">证件号码</th>
<th rowspan="1" colspan="1">手机号码</th>
</tr>
<tbody id="check_ticketInfo_id"></tbody>
</table>
<p style="color: #3177BF;" id="notice_1_id"><!--   注：1.系统将随机为您申请席位，暂不支持自选席位。-->
</p>
<div class="seat-sel seat-sel-round" id="id-seat-sel" style="display: none;"><div class="seat-sel-hd"><div class="tips-xz">选座喽</div>

						已选座<span id="selectNo">1/4</span>
</div>
<div class="seat-sel-bd"><!-- 第一排 -->
<div class="sel-item" id="yideng1" style="display: none;"><!-- 一等座-->
<div class="txt">窗</div>
<ul class="seat-list"><li><a href="javascript:" id="1A" shape="rect">A</a>
</li>
<li><a href="javascript:" id="1C" shape="rect">C</a>
</li>
</ul>
<div class="txt">过道</div>
<ul class="seat-list"><li><a href="javascript:" id="1D" shape="rect">D</a>
</li>
<li><a href="javascript:" id="1F" shape="rect">F</a>
</li>
</ul>
<div class="txt txt-last">窗</div>
</div>
<div class="sel-item" id="erdeng1" style="display: none;"><!-- 二等座-->
<div class="txt">窗</div>
<ul class="seat-list"><li><a href="javascript:" id="1A" shape="rect">A</a>
</li>
<li><a href="javascript:" id="1B" shape="rect">B</a>
</li>
<li><a href="javascript:" id="1C" shape="rect">C</a>
</li>
</ul>
<div class="txt">过道</div>
<ul class="seat-list"><li><a href="javascript:" id="1D" shape="rect">D</a>
</li>
<li><a href="javascript:" id="1F" shape="rect">F</a>
</li>
</ul>
<div class="txt txt-last">窗</div>
</div>
<div class="sel-item" id="tedeng1" style="display: none;"><!-- 特等座-->
<div class="txt">窗</div>
<ul class="seat-list"><li><a href="javascript:" id="1A" shape="rect">A</a>
</li>
<li><a href="javascript:" id="1C" shape="rect">C</a>
</li>
</ul>
<div class="txt">过道</div>
<ul class="seat-list"><li><a href="javascript:" id="1F" shape="rect">F</a>
</li>
</ul>
<div class="txt txt-last">窗</div>
</div>
<!-- 第二排 -->
<div class="sel-item" id="yideng2" style="display: none;"><!-- 一等座-->
<div class="txt">窗</div>
<ul class="seat-list"><li><a href="javascript:" id="2A" shape="rect">A</a>
</li>
<li><a href="javascript:" id="2C" shape="rect">C</a>
</li>
</ul>
<div class="txt">过道</div>
<ul class="seat-list"><li><a href="javascript:" id="2D" shape="rect">D</a>
</li>
<li><a href="javascript:" id="2F" shape="rect">F</a>
</li>
</ul>
<div class="txt txt-last">窗</div>
</div>
<div class="sel-item" id="erdeng2" style="display: none;"><!-- 二等座-->
<div class="txt">窗</div>
<ul class="seat-list"><li><a href="javascript:" id="2A" shape="rect">A</a>
</li>
<li><a href="javascript:" id="2B" shape="rect">B</a>
</li>
<li><a href="javascript:" id="2C" shape="rect">C</a>
</li>
</ul>
<div class="txt">过道</div>
<ul class="seat-list"><li><a href="javascript:" id="2D" shape="rect">D</a>
</li>
<li><a href="javascript:" id="2F" shape="rect">F</a>
</li>
</ul>
<div class="txt txt-last">窗</div>
</div>
<div class="sel-item" id="tedeng2" style="display: none;"><!-- 特等座-->
<div class="txt">窗</div>
<ul class="seat-list"><li><a href="javascript:" id="2A" shape="rect">A</a>
</li>
<li><a href="javascript:" id="2C" shape="rect">C</a>
</li>
</ul>
<div class="txt">过道</div>
<ul class="seat-list"><li><a href="javascript:" id="2F" shape="rect">F</a>
</li>
</ul>
<div class="txt txt-last">窗</div>
</div>
</div>
</div>
<div class="seat-sel seat-sel-round" id="id-bed-sel" style="display: none;"><div class="seat-sel-hd"><div class="tips-xz">选铺喽</div>

		               	 已选铺<span id="selectBedNo">1/4</span>
</div>
<div class="seat-sel-bd"><div class="sel-item"><div class="bed-yw">硬卧</div>
<div class="bed-item"><div class="txt">下铺</div>
<div class="number-control-mini"><a href="javascript:" class="num-reduce" onclick="javascript:numSet(&#39;reduce&#39;,&#39;x_no&#39;);" shape="rect">-</a>
<span class="num" id="x_no">0</span>
<a href="javascript:" class="num-increase" onclick="javascript:numSet(&#39;add&#39;,&#39;x_no&#39;);" shape="rect">+</a>
</div>
</div>
<div class="bed-item" style="display: none;" id="mid_bed"><div class="txt">中铺</div>
<div class="number-control-mini"><a href="javascript:" class="num-reduce" onclick="javascript:numSet(&#39;reduce&#39;,&#39;z_no&#39;);" shape="rect">-</a>
<span class="num" id="z_no">0</span>
<a href="javascript:" class="num-increase" onclick="javascript:numSet(&#39;add&#39;,&#39;z_no&#39;);" shape="rect">+</a>
</div>
</div>
<div class="bed-item"><div class="txt">上铺</div>
<div class="number-control-mini"><a href="javascript:" class="num-reduce" onclick="javascript:numSet(&#39;reduce&#39;,&#39;s_no&#39;);" shape="rect">-</a>
<span class="num" id="s_no">0</span>
<a href="javascript:" class="num-increase" onclick="javascript:numSet(&#39;add&#39;,&#39;s_no&#39;);" shape="rect">+</a>
</div>
</div>
</div>
</div>
</div>
<p style="color: #FF0000;" id="notice_2_id"><!--  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.根据现行规定，外国人在购买进西藏火车票时，须出示西藏自治区外事办公室或旅游局、商务厅的批准函（电），或者出示中国内地司局级接待单位出具的、已征得自治区上述部门同意的证明信函。台湾同胞赴藏从事旅游、商务活动，须事先向西藏自治区旅游局或商务厅提出申请，购买进藏火车票时须出示有关批准函。-->
</p>
<p style="color: #FF0000;" id="notice_3_id"><!--  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.按现行规定，学生票购票区间必须与学生证上的乘车区间一致，否则车站将不予换票。-->
</p>
<p style="color:#3177BF;" id="notice_4_id"><!--  *购买铁路乘意险的注册用户年龄须在18周岁以上，使用非中国居民身份证注册的用户如购买铁路乘意险，须在<a th:href="@{../modifyUser/initQueryUserInfo}" href="/otsweb/modifyUser/initQueryUserInfo">“我的12306—个人信息”</a>如实填写“出生日期”。<br />
	                 *父母为未成年子女投保，须在<a th:href="@{../view/passengers.html}" href="/otsweb/passengers/init">我的常用联系人</a>登记未成年子女的有效身份证件信息。   -->
</p>
<p style="color: #FF0000;" id="notice_5_id"><!--  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;改签或变更到站后的车票乘车日期在春运期间的，退票时一律按开车时间前不足24小时标准核收退票费。-->
</p>
<p id="sy_ticket_num_id"><!--  尊敬的旅客，本次列车您选择的席别尚有余票<strong>1135</strong>张，无座<strong>840</strong>张。特此提醒。<br /> 请确认信息是否正确。如正确请点击“确定”，系统将为您随机分配席位。-->
</p>
<div class="yzm" style="display: none;"><form id="randCodeForm_id" onsubmit="javascript:return false;" method="get" enctype="application/x-www-form-urlencoded"><ul><div id="mypasscode1" data-code_type="passenger" data-touclick-type="inside"><script>var targettype=['Z'];var targetdiv=['mypasscode1'];var targetelement=[''];</script>
<script src="/otn/resources/js/newpasscode/new.js" xml:space="preserve"></script>
</div>
</ul>
</form>
</div>
<div class="lay-btn" id="confirmDiv"><a id="back_edit_id" href="javascript:" class="btn92" shape="rect">返回修改</a>
<a href="javascript:" class="btn92s" id="qr_submit_id" shape="rect">确认</a>
</div>
</div>
</div>
</div>
<!-- 提交订单核对车票信息弹出层 end -->
<!-- 交易提示框 start  -->
<div id="transforNotice_id" style="display: none; margin-left: 30%; margin-top: 30%;"><div class="mark"></div>
<div class="up-box" id="content_transforNotice_id"><div class="up-box-hd" id="up-box-hd_id"><!--  <a id="closeTranforDialog_id" style="display: none;" href="javascript:">关闭</a>-->


				提示

				

			</div>
<div class="up-box-bd"><div class="up-con clearfix"><span class="icon i-work" id="iamge_status_id"></span>
<div class="r-txt" id="orderResultInfo_id"><!--  信息提示 -->
</div>
</div>
<div class="lay-btn" id="lay-btn_id"><!-- <a href="javascript:" id="qr_closeTranforDialog_id" style="display: none;" class="btn92s">确认</a> -->
</div>
</div>
</div>
</div>
<!--说明文字 start -->
<div class="srr-tips"><ul><li>请按乘车时所使用的有效身份证件准确、完整填写乘车填写乘车人姓名和证件号码。</li>
<li>如姓名中包含生僻字，可输入汉语拼音代替。<br clear="none" />
例如“李鵢”可输入“李shen”
			</li>
</ul>
</div>
<!--说明文字 end -->
<!--积分支付 提示信息 start -->
<div class="srr-tips"><ul><li>请按乘车时所使用的有效身份证件准确、完整填写乘车人姓名和证件号码。</li>
<li>如姓名中包含生僻字，可输入汉语拼音代替。<br clear="none" />
例如“李燊”可输入“李shen”
			</li>
<li>如您准备使用积分支付票款，请选择本人或受让人作为乘车人。</li>
<li>不支持网银和积分混合支付</li>
</ul>
</div>
<!--积分支付 提示信息 end -->
<!-- 交易提示框 end  -->
<form id="_es_hiddenform" method="post" enctype="application/x-www-form-urlencoded"><input type="hidden" name="_json_att" value="" />
</form>
</body>
</html>
<!-- 页面js模块 -->
<script xml:space="preserve">

/*<![CDATA[*/

           //common data
           var can_add = 'Y';
           var member_tourFlag = 'dc';
  		   var IsStudentDate=false;
           var init_seatTypes=[{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}];

           var defaultTicketTypes=[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u6210\u4EBA\u7968'},{'end_station_name':null,'end_time':null,'id':'2','start_station_name':null,'start_time':null,'value':'\u513F\u7AE5\u7968'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u5B66\u751F\u7968'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u6B8B\u519B\u7968'}];

           var init_cardTypes=[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u4E2D\u56FD\u5C45\u6C11\u8EAB\u4EFD\u8BC1'},{'end_station_name':null,'end_time':null,'id':'C','start_station_name':null,'start_time':null,'value':'\u6E2F\u6FB3\u5C45\u6C11\u6765\u5F80\u5185\u5730\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'G','start_station_name':null,'start_time':null,'value':'\u53F0\u6E7E\u5C45\u6C11\u6765\u5F80\u5927\u9646\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'B','start_station_name':null,'start_time':null,'value':'\u62A4\u7167'},{'end_station_name':null,'end_time':null,'id':'H','start_station_name':null,'start_time':null,'value':'\u5916\u56FD\u4EBA\u6C38\u4E45\u5C45\u7559\u8EAB\u4EFD\u8BC1'}];

           var ticket_seat_codeMap={'3':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'}],'2':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}],'1':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}],'4':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}]};

           var ticketInfoForPassengerForm={'cardTypes':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u4E2D\u56FD\u5C45\u6C11\u8EAB\u4EFD\u8BC1'},{'end_station_name':null,'end_time':null,'id':'C','start_station_name':null,'start_time':null,'value':'\u6E2F\u6FB3\u5C45\u6C11\u6765\u5F80\u5185\u5730\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'G','start_station_name':null,'start_time':null,'value':'\u53F0\u6E7E\u5C45\u6C11\u6765\u5F80\u5927\u9646\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'B','start_station_name':null,'start_time':null,'value':'\u62A4\u7167'},{'end_station_name':null,'end_time':null,'id':'H','start_station_name':null,'start_time':null,'value':'\u5916\u56FD\u4EBA\u6C38\u4E45\u5C45\u7559\u8EAB\u4EFD\u8BC1'}],'isAsync':'1','key_check_isChange':'EAB5BD53739742CBA64C47B5B262558189F3010BAD1AEBE8CA2FA33D','leftDetails':['\u786C\u5367(99.50\u5143)\u6709\u7968','\u786C\u5EA7(53.50\u5143)\u6709\u7968','\u8F6F\u5367(152.50\u5143)18\u5F20\u7968','\u65E0\u5EA7(53.50\u5143)\u65E0\u7968'],'leftTicketStr':'mGH7YKrhMuT6G2LFL%2BI%2F%2BWTWwrq7nvUNM9yO3C0GiNRHucYyOmtkn7FKmDc%3D','limitBuySeatTicketDTO':{'seat_type_codes':[{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}],'ticket_seat_codeMap':{'3':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'}],'2':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}],'1':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}],'4':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u786C\u5EA7'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u786C\u5367'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u8F6F\u5367'}]},'ticket_type_codes':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u6210\u4EBA\u7968'},{'end_station_name':null,'end_time':null,'id':'2','start_station_name':null,'start_time':null,'value':'\u513F\u7AE5\u7968'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u5B66\u751F\u7968'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u6B8B\u519B\u7968'}]},'maxTicketNum':'5','orderRequestDTO':{'adult_num':0,'apply_order_no':null,'bed_level_order_num':null,'bureau_code':null,'cancel_flag':null,'card_num':null,'channel':null,'child_num':0,'choose_seat':null,'disability_num':0,'end_time':{'date':1,'day':4,'hours':5,'minutes':2,'month':0,'seconds':0,'time':-10680000,'timezoneOffset':-480,'year':70},'exchange_train_flag':'1','from_station_name':'\u6B66\u660C','from_station_telecode':'WCN','get_ticket_pass':null,'id_mode':'Y','isShowPassCode':null,'leftTicketGenTime':null,'order_date':null,'passengerFlag':null,'realleftTicket':null,'reqIpAddress':null,'reqTimeLeftStr':null,'reserve_flag':'A','seat_detail_type_code':null,'seat_type_code':null,'sequence_no':null,'start_time':{'date':1,'day':4,'hours':0,'minutes':50,'month':0,'seconds':0,'time':-25800000,'timezoneOffset':-480,'year':70},'start_time_str':null,'station_train_code':'K81','student_num':0,'ticket_num':0,'ticket_type_order_num':null,'to_station_name':'\u957F\u6C99','to_station_telecode':'CSQ','tour_flag':'dc','trainCodeText':null,'train_date':{'date':25,'day':5,'hours':0,'minutes':0,'month':9,'seconds':0,'time':1571932800000,'timezoneOffset':-480,'year':119},'train_date_str':null,'train_location':null,'train_no':'4100000K840S','train_order':null,'trms_train_flag':null,'varStr':null},'purpose_codes':'00','queryLeftNewDetailDTO':{'BXRZ_num':'-1','BXRZ_price':'0','BXYW_num':'-1','BXYW_price':'0','EDRZ_num':'-1','EDRZ_price':'0','EDSR_num':'-1','EDSR_price':'0','ERRB_num':'-1','ERRB_price':'0','GG_num':'-1','GG_price':'0','GR_num':'-1','GR_price':'0','HBRW_num':'-1','HBRW_price':'0','HBRZ_num':'-1','HBRZ_price':'0','HBYW_num':'-1','HBYW_price':'0','HBYZ_num':'-1','HBYZ_price':'0','RW_num':'18','RW_price':'01525','RZ_num':'-1','RZ_price':'0','SRRB_num':'-1','SRRB_price':'0','SWZ_num':'-1','SWZ_price':'0','TDRZ_num':'-1','TDRZ_price':'0','TZ_num':'-1','TZ_price':'0','WZ_num':'0','WZ_price':'00535','WZ_seat_type_code':'1','YB_num':'-1','YB_price':'0','YDRZ_num':'-1','YDRZ_price':'0','YDSR_num':'-1','YDSR_price':'0','YRRB_num':'-1','YRRB_price':'0','YW_num':'66','YW_price':'00995','YYRW_num':'-1','YYRW_price':'0','YZ_num':'28','YZ_price':'00535','ZE_num':'-1','ZE_price':'0','ZY_num':'-1','ZY_price':'0','arrive_time':'0502','control_train_day':'','controlled_train_flag':null,'controlled_train_message':null,'day_difference':null,'end_station_name':null,'end_station_telecode':null,'from_station_name':'\u6B66\u660C','from_station_telecode':'WCN','is_support_card':null,'lishi':'04:12','seat_feature':'','start_station_name':null,'start_station_telecode':null,'start_time':'0050','start_train_date':'','station_train_code':'K81','to_station_name':'\u957F\u6C99','to_station_telecode':'CSQ','train_class_name':null,'train_no':'4100000K840S','train_seat_feature':'','yp_ex':''},'queryLeftTicketRequestDTO':{'arrive_time':'05:02','bigger20':'Y','exchange_train_flag':'1','from_station':'WCN','from_station_name':'\u6B66\u660C','from_station_no':'11','lishi':'04:12','login_id':null,'login_mode':null,'login_site':null,'purpose_codes':'00','query_type':null,'seatTypeAndNum':null,'seat_types':'1413','start_time':'00:50','start_time_begin':null,'start_time_end':null,'station_train_code':'K81','ticket_type':null,'to_station':'CSQ','to_station_name':'\u957F\u6C99','to_station_no':'13','train_date':'20191025','train_flag':null,'train_headers':null,'train_no':'4100000K840S','trms_train_flag':null,'useMasterPool':true,'useWB10LimitTime':true,'usingGemfireCache':false,'ypInfoDetail':'mGH7YKrhMuT6G2LFL%2BI%2F%2BWTWwrq7nvUNM9yO3C0GiNRHucYyOmtkn7FKmDc%3D'},'tour_flag':'dc','train_location':'Y2'};

           var orderRequestDTO={'adult_num':0,'apply_order_no':null,'bed_level_order_num':null,'bureau_code':null,'cancel_flag':null,'card_num':null,'channel':null,'child_num':0,'choose_seat':null,'disability_num':0,'end_time':{'date':1,'day':4,'hours':5,'minutes':2,'month':0,'seconds':0,'time':-10680000,'timezoneOffset':-480,'year':70},'exchange_train_flag':'1','from_station_name':'\u6B66\u660C','from_station_telecode':'WCN','get_ticket_pass':null,'id_mode':'Y','isShowPassCode':null,'leftTicketGenTime':null,'order_date':null,'passengerFlag':null,'realleftTicket':null,'reqIpAddress':null,'reqTimeLeftStr':null,'reserve_flag':'A','seat_detail_type_code':null,'seat_type_code':null,'sequence_no':null,'start_time':{'date':1,'day':4,'hours':0,'minutes':50,'month':0,'seconds':0,'time':-25800000,'timezoneOffset':-480,'year':70},'start_time_str':null,'station_train_code':'K81','student_num':0,'ticket_num':0,'ticket_type_order_num':null,'to_station_name':'\u957F\u6C99','to_station_telecode':'CSQ','tour_flag':'dc','trainCodeText':null,'train_date':{'date':25,'day':5,'hours':0,'minutes':0,'month':9,'seconds':0,'time':1571932800000,'timezoneOffset':-480,'year':119},'train_date_str':null,'train_location':null,'train_no':'4100000K840S','train_order':null,'trms_train_flag':null,'varStr':null};

           var init_limit_ticket_num='5';

           var oldTicketDTOs="";

           var goOrderDTO="";

           var gqComeFrom="";

           var transport_in_SF=false;
           

           if(ticketInfoForPassengerForm.tour_flag==ticket_submit_order.tour_flag.gc){

        	   oldTicketDTOs =null;

        	   gqComeFrom=null;
        	   transport_in_SF=null;

               }else if(ticketInfoForPassengerForm.tour_flag==ticket_submit_order.tour_flag.fc){
            	   goOrderDTO=null;

                   }

           $.views.helpers({
       		getUserName : function(name) {
       			 if(name.length>3){
       				name=name.substr(0,3)+'…';
       			 }
       			 return name;
       		}
       	});
 /*]]>*/

</script>
<script id="checkTicketInfoTemplate" type="text/x-jsrender" xml:space="preserve"><!--

<tr {{if tour_flag==~getTourFlagByKey('fc') || tour_flag==~getTourFlagByKey('gc')}} {{if save_status == "" }}style="display:none;"{{else}}{{/if}}{{else}}{{/if}}>

	<td align="center" >{{:#index+1}}</td>

    {{if ~isExistWZ(seat_type)}}

				<td class="no-seat">无座</td>

			{{else !~isExistWZ(seat_type)}}

				{{if seat_type_name.indexOf("（")>-1}}
				  	<td>{{>seat_type_name.substring(0,seat_type_name.indexOf("（"))}}</td>
				{{else}}
					<td>{{>seat_type_name}}</td>
				{{/if}}	

			{{else}}

				Original version only, without subtitles.

			{{/if}}

	<td>{{>ticket_type_name}}</td>

	<td title="{{>name}}">{{>~getUserName(name)}}</td>

	<td>{{>id_type_name}}</td>

	<td>{{>id_no}}</td>

	<td>{{>phone_no}}</td>

</tr>

-->
</script>
<script id="checkTicketInfoTemplate_choose" type="text/x-jsrender" xml:space="preserve"><!--

<tr {{if tour_flag==~getTourFlagByKey('fc') || tour_flag==~getTourFlagByKey('gc')}} {{if save_status == "" }}style="display:none;"{{else}}{{/if}}{{else}}{{/if}}>

	<td align="center" >{{:#index+1}}</td>
		
	{{if ~isExistWZ(seat_type)}}

			<td class="no-seat">无座</td>

	{{else !~isExistWZ(seat_type)}}
			{{if seat_type_name.indexOf("（")>-1}}
				<td>{{>seat_type_name.substring(0,seat_type_name.indexOf("（"))}}</td>
			{{else}}
				<td>{{>seat_type_name}}</td>
			{{/if}}	
	{{else}}

			Original version only, without subtitles.

	{{/if}}		


    {{if "3" == seat_type}}
		<td>
			<select style="height: 27px;FONT-SIZE: 12px;FONT-FAMILY: '宋体','Verdana';BACKGROUND-COLOR: #FFFFF0;color: #FB7403;MARGIN-LEFT: 3px;" id="ticketype_{{:#index}}">
             	<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_0" selected="selected">不限</option>
				<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_3">上铺 </option>
				<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_2">中铺 </option>
				<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_1">下铺 </option>
			</select>
		</td>
	{{else "4" == seat_type}}
		<td>
			<select style="height: 27px;FONT-SIZE: 12px;FONT-FAMILY: '宋体','Verdana';BACKGROUND-COLOR: #FFFFF0;color: #FB7403;MARGIN-LEFT: 3px;"  id="ticketype_{{:#index}}">
             	<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_0" selected="selected">不限</option>
				<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_3">上铺 </option>
				<option value="{{>seat_type}}#{{>ticket_type}}#{{>name}}#{{>id_no}}_1">下铺 </option>
			</select>
		</td>	
	{{else}}
		<td></td>	
	{{/if}}


	<td>{{>ticket_type_name}}</td>

	<td title="{{>name}}">{{>~getUserName(name)}}</td>

	<td>{{>id_type_name}}</td>

	<td>{{>id_no}}</td>

	<td>{{>phone_no}}</td>

</tr>

-->
</script>
<script id="ticketTitTemplate" type="text/x-jsrender" xml:space="preserve"><!--

<strong class="mr5">{{>date}}（{{>week}}）</strong><strong class="ml5">{{>station_train_code}}</strong>次<strong

						class="ml5">{{>from_station}}</strong>站<strong>（{{>start_time}}开）—{{>to_station}}</strong>站（{{>arrive_time}}到）

-->
</script>
<script id="ticketConTemplate" type="text/x-jsrender" xml:space="preserve"><!--

<span  id="ticket_status_id"  class="{{>wp_statu ? 's2' : 's1'}}">{{>seat_type_name}}{{if ticket_price!=""}}（<span class="colorA">￥{{>ticket_price}}</span>）{{else}}{{/if}}{{>ticket_statu}}</span> 
		

-->
</script>
<script id="djPassengerTemplate" type="text/x-jsrender" xml:space="preserve"><!--

<li>
<input   totalTimes="{{>total_times}}" typeFlag="{{>passenger_id_type_code}}"  id="djPassenger_{{>index_id}}"      
{{if passenger_id_type_code=="2"}}
  disabled="disabled" style="color:#999999" title="请修改身份信息"
{{else passenger_id_type_code!="B"}}
  {{if (total_times != "93") && (total_times != "95") && (total_times != "97")  && (total_times != "99")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{else}}
  {{if (total_times != "93") && (total_times != "98") && (total_times != "99") && (total_times != "91")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{/if}}

{{if (~getCurrentUserIdType()!=~getIdType('one'))&&(~getCurrentUserIdType()!=~getIdType('two'))}}  
  {{if (passenger_id_type_code==~getIdType('one'))||(passenger_id_type_code==~getIdType('two'))}}  disabled="disabled"
  {{else}}
  {{/if}} 
{{else}}
{{/if}}    type="checkbox" class="check"   /><label 
{{if passenger_id_type_code=="2"}}
  disabled="disabled" style="color:#999999" title="请修改身份信息"
{{else passenger_id_type_code!="B"}}
  {{if (total_times != "93") && (total_times != "95") && (total_times != "97")  && (total_times != "99")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{else}} 
  {{if (total_times != "93") && (total_times != "98") && (total_times != "99") && (total_times != "91")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{/if}} >{{>~getSuitName(passenger_name, (passenger_type == ~getTicketType('student')?true:false))}}</label>
</li>

-->
</script>
<script id="normalPassengerTemplate" type="text/x-jsrender" xml:space="preserve"><!--

<li>
<input totalTimes="{{>total_times}}" typeFlag="{{>passenger_id_type_code}}" id="normalPassenger_{{>index_id}}"      
{{if passenger_id_type_code=="2"}}
  disabled="disabled" style="color:#999999" title="请修改身份信息"
{{else passenger_id_type_code!="B"}}
  {{if (total_times != "93") && (total_times != "95") && (total_times != "97")  && (total_times != "99")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{else}} 
  {{if (total_times != "93") && (total_times != "98") && (total_times != "99")&& (total_times != "97") && (total_times != "91")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{/if}}

{{if (~getCurrentUserIdType()!=~getIdType('one'))&&(~getCurrentUserIdType()!=~getIdType('two'))&&(~getCurrentUserIdType()!=~getIdType('work'))}}  
  {{if (passenger_id_type_code==~getIdType('one'))||(passenger_id_type_code==~getIdType('two'))||(passenger_id_type_code==~getIdType('work'))}}  
	 disabled="disabled" title="不允许为该乘车人购票"
  {{/if}} 
{{/if}}    type="checkbox" class="check"   /><label 
{{if passenger_id_type_code=="2"}}
  disabled="disabled" style="color:#999999" title="请修改身份信息"
{{else passenger_id_type_code!="B"}}
  {{if (total_times != "93") && (total_times != "95") && (total_times != "97") && (total_times != "99")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{else}} 
  {{if (total_times != "93") && (total_times != "98") && (total_times != "99") && (total_times != "97")&& (total_times != "91")}} 
     disabled="disabled" style="color:#999999" title="请修改身份信息"
  {{/if}}   
{{/if}} 
{{if (~getCurrentUserIdType()!=~getIdType('one'))&&(~getCurrentUserIdType()!=~getIdType('two'))&&(~getCurrentUserIdType()!=~getIdType('work'))}}  
  {{if (passenger_id_type_code==~getIdType('one'))||(passenger_id_type_code==~getIdType('two'))||(passenger_id_type_code==~getIdType('work'))}}  
	 style="color:#999999" title="不允许为该乘车人购票"
  {{else}}
  {{/if}} 
{{else}}
{{/if}}>{{>~getSuitName(passenger_name, (passenger_type == ~getTicketType('student')?true:false))}}</label>
</li>

-->
</script>
<script id="ticketInfoTemplate" type="text/x-jsrender" xml:space="preserve"><!--

<tr id="tr_id_{{:#index+1}}">
				<td align="center">{{:#index+1}}</td>

						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}} title="不允许变更票种信息" {{else}}{{/if}}>

    <select id="ticketType_{{:#index+1}}" name="confirmTicketType" onchange="javascript:updateSeatTypeByeTickeType(this);" {{if (tour_flag == ~getTourFlagByKey('gc') || tour_flag ==~getTourFlagByKey('fc')) ||isAccompanyChild }} {{if isDisabled}}  disabled="disabled" style="color:#999999"{{else}}{{/if}}{{else}}{{/if}} >

                          {{for ticketTypes}}

 			{{if id==#parent.parent.data.ticket_type&&(#parent.parent.parent.data.IsStudentDate==true||id!=3)}}
				<option name="ticket_type_option" value="{{>id}}" selected="selected" >{{>value}}</option>
			{{else  id!=#parent.parent.data.ticket_type||id==3}}

				 <option value="{{>id}}">{{>value}} </option>

			{{else}}

			{{/if}}

				         

            {{else}}

            {{/for}}

</select>

                        </td>

			<td><select  onclick="javascript:stepFirValidatorTicketInfo(true);" id="seatType_{{:#index+1}}">

                         {{for seatTypes}}

             {{if id==#parent.parent.data.seat_type}}
				<option value="{{>id}}" selected="selected" >
                  {{if (null!=~seatTypePriceForSeatName(value))&&(""!=~seatTypePriceForSeatName(value))}}
                   {{>value}}（￥{{>~seatTypePriceForSeatName(value)}}） 
                  {{else}}
                   {{>value}}
                  {{/if}}
                </option>

			{{else  id!=#parent.parent.data.seat_type}}

				<option value="{{>id}}" >
                  {{if (null!=~seatTypePriceForSeatName(value))&&(""!=~seatTypePriceForSeatName(value))}}
                   {{>value}}（￥{{>~seatTypePriceForSeatName(value)}}）
                  {{else}}
                   {{>value}}
                  {{/if}}
                </option>

			{{else}}

				Original version only, without subtitles.

			{{/if}}

				

            {{else}}

            {{/for}}

             </select>

                         </td>

						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}}title="不允许变更乘车人信息"{{else}}{{/if}}><div class="pos-rel"><input onkeyup="javascript:elemOnkeyupNotice(this);"  id="passenger_name_{{:#index+1}}" class="inptxt w110" value="{{>name}}"   {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}}  disabled="disabled" title="不允许变更乘车人信息"  {{else}} {{/if}}  size="12" maxlength="20"/><div class="w110-focus" id="passenger_name_{{:#index+1}}_notice"></div></div></td>


						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}}title="不允许变更乘车人信息"{{else}}{{/if}}><select id="passenger_id_type_{{:#index+1}}"  {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}}  disabled="disabled" title="不允许变更乘车人信息"  style="color:#999999"  {{else}} {{/if}} >

                       {{for cardTypes ~id_type_name=id_type_name}}

 {{if id == #parent.parent.data.id_type}}

				<option value="{{>id}}" selected="selected" >{{if ~id_type_name ne ''}} {{>~id_type_name}} {{else}} {{>value}} {{/if}}</option>

			{{else  id!=#parent.parent.data.id_type}}

				 <option value="{{>id}}">{{>value}}</option>

			{{else}}

			{{/if}}

				

           {{else}}

           {{/for}}

        </select>

             </td>

<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}} title="不允许变更乘车人信息"{{else}}{{/if}}><div class="pos-rel"><input onkeyup="javascript:elemOnkeyupNotice(this);"  id="passenger_id_no_{{:#index+1}}" class="inptxt w160" value="{{>id_no}}"   {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}}  disabled="disabled" title="不允许变更乘车人信息"   {{else}} {{/if}}   size="20" maxlength="35"/><div class="w160-focus" id="passenger_id_no_{{:#index+1}}_notice"></div></div></td>

						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}} title="不允许变更乘车人信息"{{else}}{{/if}}><div class="pos-rel"><input  onkeyup="javascript:elemOnkeyupNotice(this);" id="phone_no_{{:#index+1}}" class="inptxt w110" value="{{>phone_no=='null'?'':phone_no}}"   {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}} title="不允许变更乘车人信息"  disabled="disabled"   {{else}} {{/if}}  size="11" maxlength="20"  /><div class="w160-focus" id="phone_no_{{:#index+1}}_notice"></div></div></td>



 {{if tour_flag == ~getTourFlagByKey('gc') }}
<td>
	<input id="save_{{:#parent.index+1}}" onclick="javascript:updateAllCheckBox()" type="checkbox" class="check"  {{>#parent.data.save_status}}    /> 
     {{if ~isChangeStation() }}
                变更到站
     {{else}}
               改签
     {{/if}}
      
</td>
			{{else  tour_flag==~getTourFlagByKey('fc')}}
<td>
			<input id="save_{{:#parent.index+1}}" onclick="javascript:updateAllCheckBox()" type="checkbox" class="check"  {{>#parent.data.save_status}} /> 

                返程
</td>
            {{else}}


			{{else}}

			{{/if}}
{{if (tour_flag ==  ~getTourFlagByKey('dc')  || tour_flag  == ~getTourFlagByKey('wc')) && (#data.id_no!="") && (#data.ticket_type==1|| #data.ticket_type==4) }}
	<td title="添加儿童票">
		<a href="javascript:" onClick="javascript:addChildPassengerInfo(this);" id="addchild_{{:#parent.index+1}}" name="addchild_{{>only_id}}">添加儿童票 
		</a>
		
	</td>
{{else}}
	<td style="width:40;">
		<a href="javascript:" id="addchild_{{:#parent.index+1}}" name="addchild_{{>only_id}}"></a>
	</td>
{{/if}}

{{if tour_flag ==  ~getTourFlagByKey('dc')  || tour_flag  == ~getTourFlagByKey('wc') }}

<td {{if (tour_flag == ~getTourFlagByKey('dc'))||(tour_flag == ~getTourFlagByKey('wc'))}}title="删除常用联系人"{{else}}{{/if}}>

 <span	class="i-del"  onClick="javascript:delPassengerInfo(this);" id="del_{{:#parent.index+1}}_{{>only_id}}" ></span>

</td>
{{else}}
 <td style="display:none;">

 <span  id="del_{{:#parent.index+1}}_{{>only_id}}" ></span>

</td>
{{/if}}

		</tr>

   <tr id="tr_id_{{:#index+1}}_check" class="tips"  style="display:none" >

                    <td colspan="1">&nbsp;</td>

                    <td colspan="2"><span class="txt-wrong" style="display:none" id="seatType_{{:#index+1}}_check">请输入旅客姓名</span></td>

                    <td colspan="2"><span class="txt-wrong" style="display:none" id="passenger_name_{{:#index+1}}_check">请输入旅客姓名</span></td>

                    <td colspan="1"><span class="txt-wrong" style="display:none" id="passenger_id_no_{{:#index+1}}_check">请输入旅客姓名</span></td>

                    <td colspan="3"><span class="txt-wrong" style="display:none" id="phone_no_{{:#index+1}}_check">请输入旅客姓名</span></td>

  </tr>

-->
</script>
<script id="ticketInfoTemplateForTrms" type="text/x-jsrender" xml:space="preserve"><!--

<tr id="tr_id_{{:#index+1}}">
				<td align="center">{{:#index+1}}</td>

						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}} title="不允许变更票种信息" {{else}}{{/if}}>

    <select id="ticketType_{{:#index+1}}" name="confirmTicketType" onchange="javascript:updateSeatTypeByeTickeType(this);" {{if (tour_flag == ~getTourFlagByKey('gc') || tour_flag ==~getTourFlagByKey('fc')) ||isAccompanyChild }} {{if isDisabled}}  disabled="disabled" style="color:#999999"{{else}}{{/if}}{{else}}{{/if}} >

                          {{for ticketTypes}}

 			{{if id==#parent.parent.data.ticket_type&&(#parent.parent.parent.data.IsStudentDate==true||id!=3)}}
				<option name="ticket_type_option" value="{{>id}}" selected="selected" >{{>value}}</option>
			{{else  id!=#parent.parent.data.ticket_type||id==3}}

				 <option value="{{>id}}">{{>value}} </option>

			{{else}}

			{{/if}}

				         

            {{else}}

            {{/for}}

</select>

                        </td>

			<td><div class="seat-select">
				</div>
            </td>

						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}}title="不允许变更乘车人信息"{{else}}{{/if}}><div class="pos-rel"><input onkeyup="javascript:elemOnkeyupNotice(this);"  id="passenger_name_{{:#index+1}}" class="inptxt w110" value="{{>name}}"   {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}}  disabled="disabled" title="不允许变更乘车人信息"  {{else}} {{/if}}  size="12" maxlength="20"/><div class="w110-focus" id="passenger_name_{{:#index+1}}_notice"></div></div></td>


						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}}title="不允许变更乘车人信息"{{else}}{{/if}}><select id="passenger_id_type_{{:#index+1}}"  {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}}  disabled="disabled" title="不允许变更乘车人信息"  style="color:#999999"  {{else}} {{/if}} >

                       {{for cardTypes ~id_type_name=id_type_name}}

 {{if id == #parent.parent.data.id_type}}

				<option value="{{>id}}" selected="selected" >{{if ~id_type_name ne ''}} {{>~id_type_name}} {{else}} {{>value}} {{/if}}</option>

			{{else  id!=#parent.parent.data.id_type}}

				 <option value="{{>id}}">{{>value}}</option>

			{{else}}

			{{/if}}

				

           {{else}}

           {{/for}}

        </select>

             </td>

<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}} title="不允许变更乘车人信息"{{else}}{{/if}}><div class="pos-rel"><input onkeyup="javascript:elemOnkeyupNotice(this);"  id="passenger_id_no_{{:#index+1}}" class="inptxt w160" value="{{>id_no}}"   {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}}  disabled="disabled" title="不允许变更乘车人信息"   {{else}} {{/if}}   size="20" maxlength="35"/><div class="w160-focus" id="passenger_id_no_{{:#index+1}}_notice"></div></div></td>

						<td {{if (tour_flag == ~getTourFlagByKey('gc'))||(tour_flag == ~getTourFlagByKey('fc'))}} title="不允许变更乘车人信息"{{else}}{{/if}}><div class="pos-rel"><input  onkeyup="javascript:elemOnkeyupNotice(this);" id="phone_no_{{:#index+1}}" class="inptxt w110" value="{{>phone_no=='null'?'':phone_no}}"   {{if isDisabled || ~isCanAdd()=="N" ||(#data.ticket_type==2)}} title="不允许变更乘车人信息"  disabled="disabled"   {{else}} {{/if}}  size="11" maxlength="20"  /><div class="w160-focus" id="phone_no_{{:#index+1}}_notice"></div></div></td>



 {{if tour_flag == ~getTourFlagByKey('gc') }}
<td>
	<input id="save_{{:#parent.index+1}}" onclick="javascript:updateAllCheckBox()" type="checkbox" class="check"  {{>#parent.data.save_status}}    /> 
     {{if ~isChangeStation() }}
                变更到站
     {{else}}
               改签
     {{/if}}
      
</td>
			{{else  tour_flag==~getTourFlagByKey('fc')}}
<td>
			<input id="save_{{:#parent.index+1}}" onclick="javascript:updateAllCheckBox()" type="checkbox" class="check"  {{>#parent.data.save_status}} /> 

                返程
</td>
            {{else}}


			{{else}}

			{{/if}}
{{if (tour_flag ==  ~getTourFlagByKey('dc')  || tour_flag  == ~getTourFlagByKey('wc')) && (#data.id_no!="") && (#data.ticket_type==1|| #data.ticket_type==4) }}
	<td title="添加儿童票">
		<a href="javascript:" onClick="javascript:addChildPassengerInfo(this);" id="addchild_{{:#parent.index+1}}" name="addchild_{{>only_id}}">添加儿童票 
		</a>
		
	</td>
{{else}}
	<td style="width:40;">
		<a href="javascript:" id="addchild_{{:#parent.index+1}}" name="addchild_{{>only_id}}"></a>
	</td>
{{/if}}

{{if tour_flag ==  ~getTourFlagByKey('dc')  || tour_flag  == ~getTourFlagByKey('wc') }}

<td {{if (tour_flag == ~getTourFlagByKey('dc'))||(tour_flag == ~getTourFlagByKey('wc'))}}title="删除常用联系人"{{else}}{{/if}}>

 <span	class="i-del"  onClick="javascript:delPassengerInfo(this);" id="del_{{:#parent.index+1}}_{{>only_id}}" ></span>

</td>
{{else}}
 <td style="display:none;">

 <span  id="del_{{:#parent.index+1}}_{{>only_id}}" ></span>

</td>
{{/if}}

		</tr>

   <tr id="tr_id_{{:#index+1}}_check" class="tips"  style="display:none" >

                    <td colspan="1">&nbsp;</td>

                    <td colspan="2"><span class="txt-wrong" style="display:none" id="seatType_{{:#index+1}}_check">请输入旅客姓名</span></td>

                    <td colspan="2"><span class="txt-wrong" style="display:none" id="passenger_name_{{:#index+1}}_check">请输入旅客姓名</span></td>

                    <td colspan="1"><span class="txt-wrong" style="display:none" id="passenger_id_no_{{:#index+1}}_check">请输入旅客姓名</span></td>

                    <td colspan="3"><span class="txt-wrong" style="display:none" id="phone_no_{{:#index+1}}_check">请输入旅客姓名</span></td>

  </tr>

-->
</script>
<script id="oldTicketInfoForGcTemplate" type="text/x-jsrender" xml:space="preserve"><!--
<tr>
<td>{{:#index+1}}</td>

<td>{{>train_date}}  {{>start_time}}开<br />{{>station_train_code}}{{>from_station}}-{{>to_station}}</td>

<td>{{>seat_type_name}} {{>coach_name}}车厢<br />{{>seat_name}} </td>

<td>{{>passenger_name}}<br />{{>id_type_name}}</td>

<td>{{>ticket_type_name}}<br /><span class="colorA">{{>ticket_price}}元</span></td>

</tr>

-->
</script>
"""
        html = html_page.content()

        re_repeat_submit_token = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
        re_ticket_info_for_passenger_form = re.compile(r'var ticketInfoForPassengerForm=({.+})?')
        re_order_request_dto = re.compile(r'var orderRequestDTO=({.+})?')

        repeat_submit_token = re.search(re_repeat_submit_token, html).group(1)
        ticket_info_for_passenger_form = re.search(re_ticket_info_for_passenger_form, html).group(1)
        order_request_dto = re.search(re_order_request_dto, html).group(1)

        return {
            'repeat_submit_token': repeat_submit_token,
            'ticket_info_for_passenger_form': json.loads(ticket_info_for_passenger_form.replace('\'', '\"')),
            'order_request_params': json.loads(order_request_dto.replace('\'', '\"'))
        }


if __name__ == '__main__':
    order = Order()
    order.submit(search_stack('武昌', '长沙', train_no='K81')[0], '加金安', 1)
