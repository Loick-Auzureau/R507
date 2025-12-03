from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json
import subprocess , platform
from models.host import *
from models.action import *
from models.indicator import *
from models.server import *
from database import configure_db, engine
from sqlmodel import Session, select

async def on_start_up():
    configure_db()

app = FastAPI(on_startup=[on_start_up])

@app.get("/hosts")
def read_hosts() -> list[Host]:
    with Session(engine) as session:
        hosts = session.exec(select(Host)).all()
        return hosts
    
@app.get("/host/{host_id}")
def read_host(host_id: int) -> Host:
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        return host
    
@app.post("/host")
def create_host(host: Host) -> Host:
    with Session(engine) as session:
        session.add(host)
        session.commit()
        session.refresh(host)
        return host
    
@app.delete("/host/{host_id}")
def delete_host(host_id: int) -> dict:
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}

@app.put("/host/{host_id}")
def update_host(host_id: int, updated_host: Host) -> Host:
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        host.name = updated_host.name
        host.ip = updated_host.ip
        session.add(host)
        session.commit()
        session.refresh(host)
        return host
# Endpoints pour les serveurs
@app.get("/srvs")
def read_srvs() -> list[Server]:
    with Session(engine) as session:
        srvs = session.exec(select(Server)).all()
        return srvs
    
@app.get("/srv/{srv_id}")
def read_srv(srv_id: int) -> Server:
    with Session(engine) as session:
        server = session.get(Server, srv_id)
        if not server: raise HTTPException(status_code=404, detail="Server not found")
        return server
    
@app.post("/srv")
def create_srv(server: Server) -> Server:
    with Session(engine) as session:
        session.add(server)
        session.commit()
        session.refresh(server)
        return server
    
@app.delete("/srv/{srv_id}")
def delete_srv(srv_id: int) -> dict:
    with Session(engine) as session:
        server = session.get(Server, srv_id)
        if not server: raise HTTPException(status_code=404, detail="Server not found")
        session.delete(server)
        session.commit()
        return {"ok": True}

@app.put("/srv/{srv_id}")
def update_srv(srv_id: int, updated_server: Server) -> Server:
    with Session(engine) as session:
        server = session.get(Server, srv_id)
        if not server: raise HTTPException(status_code=404, detail="Server not found")
        server.name = updated_server.name
        server.ip = updated_server.ip
        server.fonction = updated_server.fonction
        server.RAM = updated_server.RAM
        server.disk = updated_server.disk
        session.add(server)
        session.commit()
        session.refresh(server)
        return server
#--------------------------------------------------------------------
@app.get("/actions")
def get_actions() -> list[Action]:
    with Session(engine) as session:
        actions = session.exec(select(Action)).all()
        return actions
    
@app.get("/action/{action_id}")
def get_action(action_id: int) -> Action:
    with Session(engine) as session:
        action = session.get(Action, action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found")
        return action
    
@app.post("/action")
def create_action(action: Action) -> Action:
    with Session(engine) as session:
        session.add(action)
        session.commit()
        session.refresh(action)
        return action
    
@app.delete("/action/{action_id}")
def delete_action(action_id: int) -> dict:
    with Session(engine) as session:
        action = session.get(Action, action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found")
        session.delete(action)
        session.commit()
        return {"ok": True}
    
@app.put("/action/{action_id}")
def update_action(action_id: int, updated_action: Action) -> Action:
    with Session(engine) as session:
        action = session.get(Action, action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found")
        action.name = updated_action.name
        action.script_path = updated_action.script_path
        session.add(action)
        session.commit()
        session.refresh(action)
        return action
    



### Endpoints pour les indicateurs ###
@app.get("/indicators")
def get_indicators() -> list[Indicator_host]:
    with Session(engine) as session:
        indicators = session.exec(select(Indicator_host)).all()
        return indicators

@app.get("/host/{host_id}/indicators")
def get_host_indicators(host_id: int) -> list[Indicator_host]:
    with Session(engine) as session:
        indicators = session.exec(select(Indicator_host).where(Indicator_host.host_id == host_id)).all()
        return indicators
    
@app.post("/host/{host_id}/indicator")
def create_host_indicator(host_id: int, indicator: Indicator_host) -> Indicator_host:
    with Session(engine) as session:
        indicator.host_id = host_id
        session.add(indicator)
        session.commit()
        session.refresh(indicator)
        return indicator
    
@app.delete("/indicator/{indicator_id}")
@app.delete("/host/{host_id}/indicator/{indicator_id}")
def delete_indicator(host_id: int, indicator_id: int) -> dict:
    with Session(engine) as session:
        indicator = session.get(Indicator_host, indicator_id)
        if not indicator: raise HTTPException(status_code=404, detail="Indicator not found")
        session.delete(indicator)
        session.commit()
        return {"ok": True}
    
@app.get("/host/{host_id}/ping")
def ping_host(host_id: int):
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(404)
        count_flag = "-n" if platform.system().lower().startswith("win") else "-c"
        p = subprocess.run(["ping", count_flag, "1", host.ip], capture_output=True)
        return {"reachable": p.returncode == 0}

@app.get("/srv/{srv_id}/ping")
def ping_host(srv_id: int):
    with Session(engine) as session:
        srv = session.get(Server, srv_id)
        if not srv: raise HTTPException(404)
        count_flag = "-n" if platform.system().lower().startswith("win") else "-c"
        p = subprocess.run(["ping", count_flag, "1", srv.ip], capture_output=True)
        return {"reachable": p.returncode == 0}