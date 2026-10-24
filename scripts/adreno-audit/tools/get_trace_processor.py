from pathlib import Path
import urllib.request,hashlib
P=Path(__file__).parent;f=P/'trace_processor_shell'
url='https://commondatastorage.googleapis.com/perfetto-luci-artifacts/v54.0/linux-amd64/trace_processor_shell'
expected='a7aa1f738bbe2926a70f0829d00837f5720be8cafe26de78f962094fa24a3da4'
if not f.exists():f.write_bytes(urllib.request.urlopen(url,timeout=30).read())
assert hashlib.sha256(f.read_bytes()).hexdigest()==expected,'Perfetto binary checksum mismatch; refusing execution'
f.chmod(0o755);print('Perfetto v54.0 verified against the Android checkout prebuilt manifest')
