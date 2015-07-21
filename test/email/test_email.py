# -*- coding: utf-8 -*-
from cifsdk.urls import extract_urls

text = """
Delivered-To: debian@barely3am.com
Received: by 10.112.40.50 with SMTP id u18csp3284741lbk;
        Thu, 16 Apr 2015 11:26:12 -0700 (PDT)
X-Received: by 10.170.122.143 with SMTP id o137mr29172319ykb.68.1429208770601;
        Thu, 16 Apr 2015 11:26:10 -0700 (PDT)
Return-Path: <ricardo@generalstore.aw>
Received: from smtp.setarnet.aw (smtp.setarnet.aw. [209.88.129.169])
        by mx.google.com with ESMTPS id z19si4737611yhz.186.2015.04.16.11.26.09
        for <debian@barely3am.com>
        (version=TLSv1 cipher=ECDHE-RSA-RC4-SHA bits=128/128);
        Thu, 16 Apr 2015 11:26:10 -0700 (PDT)
Received-SPF: none (google.com: ricardo@generalstore.aw does not designate permitted sender hosts) client-ip=209.88.129.169;
Authentication-Results: mx.google.com;
       spf=none (google.com: ricardo@generalstore.aw does not designate permitted sender hosts) smtp.mail=ricardo@generalstore.aw
X-SENDER-REPUTATION: -4.1
X-SENDER-IP: 201.229.35.5
X-IronPort-Anti-Spam-Filtered: true
X-IronPort-Anti-Spam-Result: A2D97wAd/i9VOwUj5ckZAocAgRCvbpIYgTyHLiOBUQIBAQEIAQEBASIIBAo7QQECAoNVEBwEEQIfAjMDEAMOQAQWCgMDGQEhB4gFARUCAY0fpVoMhlKJMQGHKpIjjE6FY2KQQ4EgjE+EMYMSAg
X-IPAS-Result: A2D97wAd/i9VOwUj5ckZAocAgRCvbpIYgTyHLiOBUQIBAQEIAQEBASIIBAo7QQECAoNVEBwEEQIfAjMDEAMOQAQWCgMDGQEhB4gFARUCAY0fpVoMhlKJMQGHKpIjjE6FY2KQQ4EgjE+EMYMSAg
X-IronPort-AV: E=Sophos;i="5.11,589,1422936000";
   d="scan'208,217";a="49067414"
Received: from 201-229-35-5.static.setardsl.aw (HELO generalstore.aw) ([201.229.35.5])
  by smtp.setarnet.aw with ESMTP; 16 Apr 2015 14:25:05 -0400
thread-index: AdB4cqeDBhCNMbjzSKW+APSGAuRmpQ==
Thread-Topic: Hello
Received: from User ([176.61.137.27]) by generalstore.aw with Microsoft SMTPSVC(6.0.3790.3959); Thu, 16 Apr 2015 14:25:02 -0400
Reply-To: <celmeecarlssonn@yahoo.com>
From: "Nicole Carlsson" <ricardo@generalstore.aw>
Subject: Hello
Date: Thu, 16 Apr 2015 11:25:03 -0700
MIME-Version: 1.0
Content-Type: text/html;
	charset="Windows-1251"
Content-Transfer-Encoding: quoted-printable
X-Priority: 3
X-MSMail-Priority: Normal
X-Mailer: Microsoft Outlook Express 6.00.2600.0000
X-MimeOLE: Produced By Microsoft MimeOLE V6.00.3790.4325
Bcc:
Return-Path: <ricardo@generalstore.aw>
Message-ID: <B2F19F4F-3715-4126-8EB9-477A28034D52@general-sbs.GeneralStore.local>
Content-Class: urn:content-classes:message
X-OriginalArrivalTime: 16 Apr 2015 18:25:02.0250 (UTC) FILETIME=[A751B8A0:01D07872]
Importance: normal
Priority: normal

<HTML><HEAD><TITLE></TITLE>
</HEAD>
<BODY bgcolor=3D#FFFFFF leftmargin=3D5 topmargin=3D5 rightmargin=3D5 =
bottommargin=3D5>
<FONT size=3D2 color=3D#000000 face=3D"Arial">
<DIV>
Greetings,</DIV>
<DIV>
&nbsp;</DIV>
<DIV>
I write with earnest prayer that this email will find you well. I know =
that you will be surprise at receipt of this email from me to you. I =
don't know how you will react after reading this email to you, but I do =
hope that it makes sense to you and it met favorably to your attention.I =
am Nicole Carlsson. I am 32 years of age from Sweden. My aim of writing =
you is for us to be friends a distance friend and from there we can take =
this to next level, I write this with the purest of intentions and =
I</DIV>
<DIV>
do hope that it meets with your attention, what I seek here is a God =
fearing friend that will understand me and I will understand you and =
together be perfect friends.Please write back if you can.</DIV>
<DIV>
&nbsp;</DIV>
<DIV>
Regards,</DIV>
<DIV>
&nbsp;</DIV>
<DIV>
Nicole.</DIV>
</FONT><P>&nbsp;The information in this email is confidential and =
intended solely for=20
the<BR>addressee(s). Any views or opinions presented are solely those of =
the=20
author and<BR>do not necessarily represent those of&nbsp;General =
Store&nbsp;or=20
its subsidiaries. If you<BR>are not the intended recipient, be advised =
that you=20
have received this email in<BR>error and that any disclosure, =
distribution,=20
printing, forwarding or copying is<BR>prohibited and may be =
unlawful.</P>
<P>Please notify the sender if you have received this email in =
error.<BR>General=20
Store&nbsp;and subsidiaries are not liable for the proper and=20
complete<BR>transmission of the information contained in this =
communication, or=20
for any delay<BR>in its receipt.<BR></P><div =
style=3D"color:#999999;font-size:11px;font-family:verdana"><br>Disclaimer=
 added by <b>CodeTwo Exchange Rules</b><br><a =
href=3D"http://www.codetwo.com">www.codetwo.com</a></div><br></BODY></HTM=
L>
"""

test2 = """
Delivered-To: support@barely3am.com
Received: by 10.112.40.50 with SMTP id u18csp916705lbk;
        Sun, 19 Apr 2015 05:50:04 -0700 (PDT)
X-Received: by 10.42.151.4 with SMTP id c4mr13784232icw.77.1429447803846;
        Sun, 19 Apr 2015 05:50:03 -0700 (PDT)
Return-Path: <advertisebz09ua@gmail.com>
Received: from gmail.com ([61.72.137.254])
        by mx.google.com with SMTP id s93si13575887ioe.52.2015.04.19.05.50.00
        for <support@barely3am.com>;
        Sun, 19 Apr 2015 05:50:03 -0700 (PDT)
Received-SPF: softfail (google.com: domain of transitioning advertisebz09ua@gmail.com does not designate 61.72.137.254 as permitted sender) client-ip=61.72.137.254;
Authentication-Results: mx.google.com;
       spf=softfail (google.com: domain of transitioning advertisebz09ua@gmail.com does not designate 61.72.137.254 as permitted sender) smtp.mail=advertisebz09ua@gmail.com;
       dmarc=fail (p=NONE dis=NONE) header.from=gmail.com
Message-ID: <BE5B7E8D.883B43A2@gmail.com>
Date: Sun, 19 Apr 2015 05:24:33 -0700
Reply-To: "HENRY" <advertisebz09ua@gmail.com>
From: "HENRY" <advertisebz09ua@gmail.com>
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.19) Gecko/20081209 Thunderbird/2.0.0.19
MIME-Version: 1.0
To: <support@barely3am.com>
Subject: Boost Social Presence with FB posts likes
Content-Type: text/plain;
    charset="us-ascii"
Content-Transfer-Encoding: 7bit

Hello,
Boost your Facebook posts with a massive promotion
and gain over 10.000 likes in total towards all your posts.

We can promote up to 20 posts links at a time.

Increase exposure with guaranteed promotion service.

Use this coupon and get another 10% discount on your purchase

==================
10% Coupon = EB2CA
==================

Order today, cheap and guaranteed service:
http://www.socialservices.cn/detail.php?id=9

Regards
HENRY
Â 






Unsubscribe option is available on the footer of our website



"""


def test_email():
    assert "http://www.codetwo.com" in extract_urls(text, html=True)
    #assert "http://www.socialservices.cn/detail.php?id=9" in extract_urls(test2)


if __name__ == '__main__':
    test_email()
