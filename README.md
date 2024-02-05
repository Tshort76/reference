# reference
A collection of reference notes/material for systems, software, processes, and techniques.

- [Computation](./Computation)
- [Data_Systems](./Data_Systems)
  - [Databases](./Data_Systems/Databases)
  - [Ops](./Data_Systems/Ops)
- [Dev_Ops](./Dev_Ops)
  - [Cloud_Providers](./Dev_Ops/Cloud_Providers)
    - [aws](./Dev_Ops/Cloud_Providers/aws)
    - [gcp](./Dev_Ops/Cloud_Providers/gcp)
      - [examples](./Dev_Ops/Cloud_Providers/gcp/examples)
- [Machine_Learning](./Machine_Learning)
  - [from_scratch](./Machine_Learning/from_scratch)
  - [walkthroughs](./Machine_Learning/walkthroughs)
- [Software_Engineering](./Software_Engineering)
  - [Clojure](./Software_Engineering/Clojure)
    - [basic_http_service](./Software_Engineering/Clojure/basic_http_service)
    - [sandbox](./Software_Engineering/Clojure/sandbox)
    - [webservice_template](./Software_Engineering/Clojure/webservice_template)
  - [Interview_Prep](./Software_Engineering/Interview_Prep)
  - [Python](./Software_Engineering/Python)
    - [utils](./Software_Engineering/Python/utils)
    - [vtk](./Software_Engineering/Python/vtk)


To regenerate project table of contents
```python
import os

def _dive_into(filename: str):
    return not (filename.startswith("resources") or filename.startswith("src") or filename.startswith("images") or filename.startswith(".") or filename.startswith("_"))

def list_dirR(d: str) -> list[str]:
    for f in os.listdir(d):
        fpath = os.path.join(d,f)
        if os.path.isdir(fpath):
            if _dive_into(f):
                dirs = fpath[len(ref_dir)+1:].split(os.path.sep)
                pre = "  "*(len(dirs)-1) + "- "
                print(f"{pre}[{dirs[-1]}](./{'/'.join(dirs)})")
                list_dirR(fpath)

list_dirR(os.getcwd())
```