import json, os, urllib.request, urllib.parse, datetime
U = "https://jsmikecorp-moatown.goatcounter.com/api/v0/stats/hits"
SITES = [("qa","모아타운 Q&A 검색",["/moatown-qa","/모아타운 Q&A 검색"],"https://jsmikecorp.github.io/moatown-qa/"),
         ("dues","모아타운 회비 조회",["/moatown-dues","/모아타운 회비 조회"],"https://jsmikecorp.github.io/moatown-dues/"),
         ("owner","모아타운 소유주 조회",["/samsung-moatown","/모아타운 소유주 조회"],"https://jsmikecorp.github.io/samsung-moatown/"),
         ("golf","골프장현황조회",["/golf-courses","/골프장현황조회"],"https://jsmikecorp.github.io/golf-courses/")]
tok = os.environ["GOATCOUNTER_API_TOKEN"]
now = datetime.datetime.now(datetime.timezone.utc)
q = urllib.parse.urlencode({"start":"2026-10-01T00:00:00Z","end":now.strftime("%Y-%m-%dT%H:%M:%SZ"),"limit":100,"daily":"true"})
req = urllib.request.Request(U+"?"+q, headers={"Authorization":"Bearer "+tok,"Content-Type":"application/json"})
hits = json.load(urllib.request.urlopen(req))["hits"]
out = []
for sid, name, paths, url in SITES:
    days = {}
    for h in hits:
        if h["path"] in paths:
            for s in h["stats"]:
                if s["daily"]: days[s["day"]] = days.get(s["day"],0)+s["daily"]
    out.append({"id":sid,"name":name,"url":url,"days":dict(sorted(days.items()))})
json.dump({"updated":now.isoformat(),"sites":out}, open("data.json","w"), ensure_ascii=False, indent=1)
print("total", sum(sum(s["days"].values()) for s in out))
