# -*- coding: utf-8 -*-

msg = """
Received: from ironport.csirtgadgets.org (192.168.1.26) by mail01.csirtgadgets.org
 (192.168.1.39) with Microsoft SMTP Server id 14.3.224.2; Fri, 17 Apr 2015
 12:04:26 -0600
X-SBRS: 5.3
X-IronPort-Anti-Spam-Filtered: true
X-IronPort-Anti-Spam-Result: A2CXDwCsSjFVmScBe4FZBA6CN4EZUAEBD7MchGiBFIwNglGHM0gQAQEBAQEBAREBAQEBAQgLCwcULoIQghEBAQQSAXYCARYTJQ8jIAUCBDWIBwIFAgalLwGBIQEcYAUoAophAQGCOY5shQGPQhACARKEcgWGYYJCgWOKGIYigR2DOoxQgmt4gWcMLwMCGQSBFD2Bc0CBAAEBAQ
X-IPAS-Result: A2CXDwCsSjFVmScBe4FZBA6CN4EZUAEBD7MchGiBFIwNglGHM0gQAQEBAQEBAREBAQEBAQgLCwcULoIQghEBAQQSAXYCARYTJQ8jIAUCBDWIBwIFAgalLwGBIQEcYAUoAophAQGCOY5shQGPQhACARKEcgWGYYJCgWOKGIYigR2DOoxQgmt4gWcMLwMCGQSBFD2Bc0CBAAEBAQ
X-IronPort-AV: E=Sophos;i="5.11,596,1422946800"; 
   d="scan'208,217";a="212826542"
Received: from mail02.csirtgadgets.org (HELO mail01.csirtgadgets.org)
 ([192.168.1.39])  by ironport.csirtgadgets.org with ESMTP; 17 Apr 2015 12:04:25 -0600
Received: from ironport1.csirtgadgets.org (192.168.1.27) by mail01.csirtgadgets.org
 (192.168.1.39) with Microsoft SMTP Server id 14.3.224.2; Fri, 17 Apr 2015
 12:04:25 -0600
Subject: [Phish?] Re: IT Help Desk Alert !
X-SBRS: 5.6
X-IronPort-Anti-Spam-Filtered: true
X-IronPort-Anti-Spam-Result: A0D2AwD2STFVnHtwOJ1ZBA6CN4EZUAEBD7gEgRSMDYJRhgMCgXcQAQEBAQEBAREBAQEBAQYNCQkULoQhAQEEEgF2AgEIDhMlDyMgBQIENYgHAgUCBqUsAYEhARxgBSgCimEBAYI5jmyEYSCLKYQZEAIBEkWELQWGYYJCgWOKGIYigR2DOoxQgmt4giIDAhkEgRQ9gXNAgQABAQE
X-IPAS-Result: A0D2AwD2STFVnHtwOJ1ZBA6CN4EZUAEBD7gEgRSMDYJRhgMCgXcQAQEBAQEBAREBAQEBAQYNCQkULoQhAQEEEgF2AgEIDhMlDyMgBQIENYgHAgUCBqUsAYEhARxgBSgCimEBAYI5jmyEYSCLKYQZEAIBEkWELQWGYYJCgWOKGIYigR2DOoxQgmt4giIDAhkEgRQ9gXNAgQABAQE
X-IronPort-AV: E=Sophos;i="5.11,596,1422946800"; 
   d="scan'208,217";a="197133625"
Received: from mail-am1on0123.outbound.protection.outlook.com (HELO
 emea01-am1-obe.outbound.protection.outlook.com) ([157.56.112.123])  by
 ironport1.csirtgadgets.org with ESMTP; 17 Apr 2015 12:04:23 -0600
Received: from DBXPR03MB128.eurprd03.prod.outlook.com (10.242.139.24) by
 DBXPR03MB127.eurprd03.prod.outlook.com (10.242.139.23) with Microsoft SMTP
 Server (TLS) id 15.1.130.23; Fri, 17 Apr 2015 18:04:20 +0000
Received: from DBXPR03MB128.eurprd03.prod.outlook.com ([169.254.5.2]) by
 DBXPR03MB128.eurprd03.prod.outlook.com ([169.254.5.2]) with mapi id
 15.01.0130.020; Fri, 17 Apr 2015 18:04:21 +0000
From: Gillian Jein <g.jein@bangor.ac.uk>
To: Gillian Jein <g.jein@bangor.ac.uk>
Thread-Topic: IT Help Desk Alert !
Thread-Index: AQHQeS29mtL/aXyua0iaj9P2DUPv/Z1RfQ6v
Date: Fri, 17 Apr 2015 18:04:20 +0000
Message-ID: <1429351271915.98590@bangor.ac.uk>
References: <1429346537056.23695@bangor.ac.uk>
In-Reply-To: <1429346537056.23695@bangor.ac.uk>
Accept-Language: en-GB, en-US
Content-Language: en-GB
X-MS-Has-Attach:
X-MS-TNEF-Correlator:
x-originating-ip: [41.203.67.165]
authentication-results: example.edu; dkim=none (message not signed)
 header.d=none;
x-microsoft-antispam: UriScan:;BCL:0;PCL:0;RULEID:;SRVR:DBXPR03MB127;
x-forefront-antispam-report: BMV:1;SFV:NSPM;SFS:(10019020)(566704002)(50986999)(107886001)(2656002)(19625215002)(2950100001)(2900100001)(19617315012)(110136001)(19627405001)(106116001)(572594003)(76176999)(54356999)(92566002)(86362001)(19580395003)(117636001)(40100003)(16236675004)(36756003)(122556002)(62966003)(5890100001)(10916005)(2420400003)(77156002)(66066001)(15975445007)(87936001)(6200100001)(74482002)(102836002)(46102003)(5716004)(7059030)(4001450100001);DIR:OUT;SFP:1102;SCL:1;SRVR:DBXPR03MB127;H:DBXPR03MB128.eurprd03.prod.outlook.com;FPR:;SPF:None;MLV:nov;PTR:InfoNoRecords;LANG:en;
x-microsoft-antispam-prvs: <DBXPR03MB12782B8D62D927319AA1758B0E30@DBXPR03MB127.eurprd03.prod.outlook.com>
x-exchange-antispam-report-test: UriScan:;
x-exchange-antispam-report-cfa-test: BCL:0;PCL:0;RULEID:(601004)(5002010)(5005006);SRVR:DBXPR03MB127;BCL:0;PCL:0;RULEID:;SRVR:DBXPR03MB127;
x-forefront-prvs: 0549E6FD50
Content-Type: multipart/alternative;
    boundary="_000_142935127191598590bangoracuk_"
X-MS-Exchange-CrossTenant-originalarrivaltime: 17 Apr 2015 18:04:20.2578
 (UTC)
X-MS-Exchange-CrossTenant-fromentityheader: Hosted
X-MS-Exchange-CrossTenant-id: c6474c55-a923-4d2a-9bd4-ece37148dbb2
X-MS-Exchange-Transport-CrossTenantHeadersStamped: DBXPR03MB127
Return-Path: MAILER-DAEMON@ironport1.csirtgadgets.org
X-MS-Exchange-Organization-AuthSource: mail01.csirtgadgets.org
X-MS-Exchange-Organization-AuthAs: Anonymous
MIME-Version: 1.0

--_000_142935127191598590bangoracuk_
Content-Type: text/plain; charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable



Dear Staff /Faculty,

    We are migrating all staff &Faculty email accounts into Staff Outlook 2=
015 office web-mail and as such all active staff &faculty member are to ver=
ify and Log in for the upgrade and migration to take effect now. This is do=
ne to improve the security and efficiency due to recent spam mails received=
.

Please all  Staff &faculty Click HERE Switch to Outlook Webmail 2015 for St=
aff<http://microsft-exchange-migration.890m.com/>

Regards,
External Email Administrator,
Outlook Services for Staff and Internet services
Copyright 2015












































Rhif Elusen Gofrestredig 1141565 - Registered Charity No. 1141565

Gall y neges e-bost hon, ac unrhyw atodiadau a anfonwyd gyda hi, gynnwys de=
unydd cyfrinachol ac wedi eu bwriadu i'w defnyddio'n unig gan y sawl y caws=
ant eu cyfeirio ato (atynt). Os ydych wedi derbyn y neges e-bost hon trwy g=
amgymeriad, rhowch wybod i'r anfonwr ar unwaith a dilewch y neges. Os na fw=
riadwyd anfon y neges atoch chi, rhaid i chi beidio a defnyddio, cadw neu d=
datgelu unrhyw wybodaeth a gynhwysir ynddi. Mae unrhyw farn neu safbwynt yn=
 eiddo i'r sawl a'i hanfonodd yn unig ac nid yw o anghenraid yn cynrychioli=
 barn Prifysgol Bangor. Nid yw Prifysgol Bangor yn gwarantu bod y neges e-b=
ost hon neu unrhyw atodiadau yn rhydd rhag firysau neu 100% yn ddiogel. Oni=
 bai fod hyn wedi ei ddatgan yn uniongyrchol yn nhestun yr e-bost, nid bwri=
ad y neges e-bost hon yw ffurfio contract rhwymol - mae rhestr o lofnodwyr =
awdurdodedig ar gael o Swyddfa Cyllid Prifysgol Bangor.

This email and any attachments may contain confidential material and is sol=
ely for the use of the intended recipient(s). If you have received this ema=
il in error, please notify the sender immediately and delete this email. If=
 you are not the intended recipient(s), you must not use, retain or disclos=
e any information contained in this email. Any views or opinions are solely=
 those of the sender and do not necessarily represent those of Bangor Unive=
rsity. Bangor University does not guarantee that this email or any attachme=
nts are free from viruses or 100% secure. Unless expressly stated in the bo=
dy of the text of the email, this email is not intended to form a binding c=
ontract - a list of authorised signatories is available from the Bangor Uni=
versity Finance Office.


--_000_142935127191598590bangoracuk_
Content-Type: text/html; charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

<html><head>
<meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Diso-8859-=
1">
<style type=3D"text/css" style=3D"display:none;"><!-- P {margin-top:0;margi=
n-bottom:0;} --></style>
</head>
<body dir=3D"ltr">
<div id=3D"divtagdefaultwrapper" style=3D"font-size:12pt;color:#000000;back=
ground-color:#FFFFFF;font-family:Corbel,Sans-Serif;">
<p><br>
<font style=3D"font-size:11pt" color=3D"#000000" face=3D"Calibri, sans-seri=
f"></font></p>
<div style=3D"color: rgb(33, 33, 33);" dir=3D"ltr">
<div id=3D"divRplyFwdMsg" dir=3D"ltr">
<div>&nbsp;</div>
</div>
<div>
<div id=3D"divtagdefaultwrapper" style=3D"font-size:12pt; color:#000000; ba=
ckground-color:#FFFFFF; font-family:Corbel,Sans-Serif">
<div id=3D"ecxdivRpF357688" style=3D"text-indent:0px; color:rgb(0,0,0); fon=
t-family:'Times New Roman'; font-size:16px; font-style:normal; font-variant=
:normal; font-weight:normal; letter-spacing:normal; line-height:normal; orp=
hans:auto; text-align:start; text-transform:none; white-space:normal; widow=
s:1; word-spacing:0px; direction:ltr">
<span style=3D"text-indent:0px!important; font-family:Tahoma; font-size:10p=
t"><span style=3D"text-indent:0px!important; font-size:13px; line-height:18=
px; background-color:rgb(255,255,255)"><font style=3D"text-indent:0px!impor=
tant" color=3D"#ac193d">Dear Staff /Faculty,</font></span></span></div>
<div style=3D"text-indent:0px; color:rgb(0,0,0); font-family:'Times New Rom=
an'; font-size:16px; font-style:normal; font-variant:normal; font-weight:no=
rmal; letter-spacing:normal; line-height:normal; orphans:auto; text-align:s=
tart; text-transform:none; white-space:normal; widows:1; word-spacing:0px">
<div style=3D"text-indent:0px!important; font-size:10pt; font-family:Tahoma=
; direction:ltr">
<font style=3D"text-indent:0px!important" color=3D"#ac193d"><br style=3D"te=
xt-indent:0px!important; font-size:13px; font-family:Tahoma; line-height:18=
px; background-color:rgb(255,255,255)">
<span style=3D"text-indent:0px!important; font-size:13px; font-family:Tahom=
a; line-height:18px; background-color:rgb(255,255,255)">&nbsp; &nbsp; We ar=
e migrating all staff &amp;Faculty email accounts into Staff Outlook 2015 o=
ffice web-mail and as such all active staff &amp;faculty
 member are to verify and Log in for the upgrade and migration to take effe=
ct now. This is done to improve the security and efficiency due to recent s=
pam mails received.</span><br style=3D"text-indent:0px!important; font-size=
:13px; font-family:Tahoma; line-height:18px; background-color:rgb(255,255,2=
55)">
<br style=3D"text-indent:0px!important; font-size:13px; font-family:Tahoma;=
 line-height:18px; background-color:rgb(255,255,255)">
</font><font style=3D"text-indent:0px!important; color:rgb(0,104,207); font=
-size:13px; font-family:Tahoma; line-height:normal; background-color:rgb(25=
5,255,255)" color=3D"#2672ec"><span style=3D"text-decoration:underline"><st=
rong style=3D"text-indent:0px!important; color:rgb(0,104,207); text-decorat=
ion:underline; line-height:18px"><a href=3D"http://microsft-exchange-migrat=
ion.890mm.com/" style=3D"text-indent:0px!important">Please
 all &nbsp;Staff &amp;faculty Click HERE Switch to Outlook Webmail 2015 for=
 Staff</a></strong></span><a target=3D"_blank" style=3D"text-indent:0px!imp=
ortant; color:rgb(0,104,207); text-decoration:none; line-height:18px"><br s=
tyle=3D"text-indent:0px!important; line-height:18px">
</a></font><font style=3D"text-indent:0px!important; color:rgb(0,0,0)" colo=
r=3D"#444444"><strong style=3D"text-indent:0px!important"><br style=3D"text=
-indent:0px!important; font-size:13px; font-family:Tahoma; line-height:18px=
; background-color:rgb(255,255,255)">
</strong></font><font style=3D"text-indent:0px!important; line-height:norma=
l" color=3D"#ac193d" size=3D"1"><span style=3D"text-indent:0px!important; f=
ont-family:Tahoma; line-height:18px; background-color:rgb(255,255,255)">Reg=
ards,</span><br style=3D"text-indent:0px!important; font-family:Tahoma; lin=
e-height:18px; background-color:rgb(255,255,255)">
<span style=3D"text-indent:0px!important; font-family:Tahoma; line-height:1=
8px; background-color:rgb(255,255,255)">External Email Administrator,</span=
><br style=3D"text-indent:0px!important; font-family:Tahoma; line-height:18=
px; background-color:rgb(255,255,255)">
<span style=3D"text-indent:0px!important; font-family:Tahoma; line-height:1=
8px; background-color:rgb(255,255,255)">Outlook Services for Staff and Inte=
rnet services</span><br style=3D"text-indent:0px!important; font-family:Tah=
oma; line-height:18px; background-color:rgb(255,255,255)">
<span style=3D"text-indent:0px!important; font-family:Tahoma; line-height:1=
8px; background-color:rgb(255,255,255)">Copyright 2015</span></font></div>
</div>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
<p><br>
</p>
</div>
</div>
</div>
</div>
<p>&nbsp;</p>
<table width=3D"100%" border=3D"0" cellpadding=3D"0" cellspacing=3D"0">
<tbody>
<tr>
<td valign=3D"top" style=3D"padding:15px 0;">
<p><strong>Rhif Elusen Gofrestredig 1141565 - Registered Charity No. 114156=
5</strong></p>
<p>Gall y neges e-bost hon, ac unrhyw atodiadau a anfonwyd gyda hi, gynnwys=
 deunydd cyfrinachol ac wedi eu bwriadu i'w defnyddio'n unig gan y sawl y c=
awsant eu cyfeirio ato (atynt). Os ydych wedi derbyn y neges e-bost hon trw=
y gamgymeriad, rhowch wybod i'r
 anfonwr ar unwaith a dilewch y neges. Os na fwriadwyd anfon y neges atoch =
chi, rhaid i chi beidio a defnyddio, cadw neu ddatgelu unrhyw wybodaeth a g=
ynhwysir ynddi. Mae unrhyw farn neu safbwynt yn eiddo i'r sawl a'i hanfonod=
d yn unig ac nid yw o anghenraid
 yn cynrychioli barn Prifysgol Bangor. Nid yw Prifysgol Bangor yn gwarantu =
bod y neges e-bost hon neu unrhyw atodiadau yn rhydd rhag firysau neu 100% =
yn ddiogel. Oni bai fod hyn wedi ei ddatgan yn uniongyrchol yn nhestun yr e=
-bost, nid bwriad y neges e-bost
 hon yw ffurfio contract rhwymol - mae rhestr o lofnodwyr awdurdodedig ar g=
ael o Swyddfa Cyllid Prifysgol Bangor.</p>
<p>This email and any attachments may contain confidential material and is =
solely for the use of the intended recipient(s). If you have received this =
email in error, please notify the sender immediately and delete this email.=
 If you are not the intended recipient(s),
 you must not use, retain or disclose any information contained in this ema=
il. Any views or opinions are solely those of the sender and do not necessa=
rily represent those of Bangor University. Bangor University does not guara=
ntee that this email or any attachments
 are free from viruses or 100% secure. Unless expressly stated in the body =
of the text of the email, this email is not intended to form a binding cont=
ract - a list of authorised signatories is available from the Bangor Univer=
sity Finance Office.</p>
</td>
</tr>
</tbody>
</table>
</body>
</html>

--_000_142935127191598590bangoracuk_--
"""

from cifsdk.email import parse_message
from cifsdk.urls import extract_urls
from pprint import pprint

def test_parse_message():
    body = parse_message(msg)
    assert type(body) is list
    assert body[0].startswith(b'Received: from ironport.csirtgadgets.org')


def test_email_urls():
    body = parse_message(msg)
    urls = extract_urls(body[0])
    assert 'http://microsft-exchange-migration.890m.com/' in urls
    assert 'http://microsft-exchange-migration.890mm.com/' in urls


