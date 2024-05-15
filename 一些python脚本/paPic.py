import requests

headers={
    'Cookie':'BDqhfp=%E5%8D%A0%E9%81%93%E7%BB%8F%E8%90%A5%26%260-10-1undefined%26%267548%26%266; BAIDUID_BFESS=87E38362360B4AC0B6EA826E887517DE:FG=1; __bid_n=18ccd0f86e161288b3fdec; BDUSS=M3djEyR1JmQ1dtTE9iR3l5YmVCZ1d-UGpHSERaQVZvNjNrUGRpVW56R1JUYnhsRVFBQUFBJCQAAAAAAAAAAAEAAADHXS7dvLW2yrreMTkxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJHAlGWRwJRlV0; BDUSS_BFESS=M3djEyR1JmQ1dtTE9iR3l5YmVCZ1d-UGpHSERaQVZvNjNrUGRpVW56R1JUYnhsRVFBQUFBJCQAAAAAAAAAAAEAAADHXS7dvLW2yrreMTkxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJHAlGWRwJRlV0; BIDUPSID=87E38362360B4AC0B6EA826E887517DE; PSTM=1704697699; H_PS_PSSID=39996_40045; ZFY=u0ClttB8owEVqx45:BHjqitXN6NDRjeT0lhugJGFQ9EU:C; newlogin=1; jsdk-uuid=1158fba9-4b74-456d-b678-7f7f84d8a62a; RT="z=1&dm=baidu.com&si=1bc6f645-ead6-4e80-b6c8-b2d503a8f792&ss=lriyi8lq&sl=b&tt=3zy&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1fm2i"; ai-studio-ticket=47FF3955D792468896CC4D852A5DBC3BEC12D24303284BE480B7E51E5F5247E3; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; cleanHistoryStatus=0; indexPageSugList=%5B%22%E5%8D%A0%E9%81%93%E7%BB%8F%E8%90%A5%22%2C%22%E5%85%A8%E9%83%A8%22%5D; BA_HECTOR=8kak2g0ha10h2080008l840l71r5m31iqkas61t; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; delPer=0; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; firstShowTip=1; userFrom=cn.bing.com; ab_sr=1.0.1_NzFmNzdkNDEyMjk4Y2U4NTUzMTAxN2FiMzdkODI3MDYxODQzMmE2ZDM3YWU3OTM2MDVhZTAyMTNkM2FlMWI1MjhlZjMyYjVjYmEzNTBhNWQ1Njg2NzJlN2IwYWEzYzk3YzgyMDM3NDY4ZjVhMjAxNzcyY2RlZTQ1MjE0ODI1NDIxNzM1YzJhODkwM2E3MTBjNDQ4NTU4NWY5MjRiODI2Mg==',
    'Referer':"https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwxLDIsMyw2LDQsNSw3LDgsOQ%3D%3D&word=%E5%8D%A0%E9%81%93%E7%BB%8F%E8%90%A5",
    'Host':'image.baidu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}
num=103
for page in range(1,201):
    url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8655859733730011355&ipn=rj&ct=201326592&is=&fp=result&fr=&word=%E8%A1%97%E9%81%93%E7%A7%AF%E6%B0%B4%E6%80%8E%E4%B9%88%E5%8A%9E&queryWord=%E8%A1%97%E9%81%93%E7%A7%AF%E6%B0%B4%E6%80%8E%E4%B9%88%E5%8A%9E&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={page*30}&rn=30&gsm=3c&1713151256908='
    response = requests.get(url=url, headers=headers)
    json_data = response.json()
    datalist = json_data['data']
    for data in datalist[:-1]:
        middleURL = data['middleURL']
        # print(middleURL)
        img_data = requests.get(url=middleURL).content
        with open(f'D:/shuju/pa/新村/测试图片/路面积水/testWater{num}.jpg', "wb") as f:
            f.write(img_data)
            num += 1

