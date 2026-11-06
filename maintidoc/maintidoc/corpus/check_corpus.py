import csv, re, subprocess, sys, os, json
sys.path.insert(0,"/tmp/claude-0/-home-claude/ea3944d4-23bb-5e9e-be10-782ca6328510/scratchpad/build")
from data import ALARMS, HISTORY, EQUIP
ROOT=sys.argv[1]; INV=sys.argv[2]
rows=list(csv.DictReader(open(INV)))
def pages_text(f):
    t=subprocess.run(["pdftotext","-layout",f,"-"],capture_output=True,text=True).stdout
    return t.split("\f")[:-1] if t.strip() else []
def npages(f):
    return int([l for l in subprocess.run(["pdfinfo",f],capture_output=True,text=True).stdout.splitlines() if l.startswith("Pages")][0].split()[1])
err=0; tot=0
for r in rows:
    f=os.path.join(ROOT,r["fichier"]); 
    if not os.path.exists(f): print("MANQUE",f); err+=1; continue
    tot+=1
    n=1 if f.endswith(".jpg") else npages(f)
    if str(n)!=r["nb_pages"]: print("PAGES",r["document_id"],n,r["nb_pages"]); err+=1
    if f.endswith(".pdf"):
        pt=pages_text(f); txt=" ".join(pt)
        scanned=r["format"]=="pdf_scanne"
        if scanned and txt.strip(): print("SCAN a du texte",r["document_id"]); err+=1
        if not scanned and not txt.strip(): print("PAS DE TEXTE",r["document_id"]); err+=1
        did=r["document_id"]
        if did.startswith(("manuel_","codes_alarme_")):
            mod={"perf_a":"InfuPro 300","perf_b":"InfuPro 500","mon_a":"VitaScan M200","mon_b":"VitaScan M400"}[[k for k in ("perf_a","perf_b","mon_a","mon_b") if did.endswith(k)][0]]
            al=[a for a in ALARMS if a[0]==mod]
            for a in al:
                if did.startswith("manuel_"):
                    p=a[6]
                    if not re.search(rf"\b{a[1]}\b",pt[p-1]) or a[2] not in pt[p-1].replace("\n"," ").replace("  "," ") and a[2].split()[0] not in pt[p-1]: print("CODE ABSENT PAGE",did,a[1],p); err+=1
                    for q,tp in enumerate(pt,1):
                        if q!=p and re.search(rf"^\s*{a[1]}\s",tp,re.M): print("CODE SUR AUTRE PAGE",did,a[1],q); err+=1
            allowed={a[1] for a in al}
            found=set(re.findall(r"\bE\d{3}\b",txt))
            if found-allowed: print("CODE HORS MODELE",did,found-allowed); err+=1
        else:
            found=set(re.findall(r"\bE\d{3}\b",txt))
            allc={a[1] for a in ALARMS}
            if found-allc: print("CODE INCONNU",r["document_id"],found-allc); err+=1
        for m in re.findall(r"\b(?:PERF|MON)-[AB]-\d\d\b",txt):
            if m not in {e[0] for e in EQUIP}: print("ID INCONNU",did,m); err+=1
        for m in re.findall(r"\bTK-\d{4}\b",txt):
            if m not in {h[5] for h in HISTORY}: print("TICKET INCONNU",did,m); err+=1
        for m in re.findall(r"\b(?:IP3|IP5|VS2|VS4)-\d\d-\d{4}\b",txt):
            if m not in {e[2] for e in EQUIP}: print("SERIE INCONNUE",did,m); err+=1
print("fichiers",tot,"erreurs",err)
