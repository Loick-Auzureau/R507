from typing import Optional
from sqlmodel import Field, SQLModel

class Server(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: str
    fonction: str
    nbr_cpu: int
    RAM: int = 0
    disk: int = 0

    def __str__(self):
        return f"#{self.id} | Server {self.name} d'ip {self.ip} utilisé comme {self.fonction} avec un cpu de {self.nbr_cpu} coeurs, {self.RAM}Go de RAM,{self.disk}To de ROM"
    
    def __repr__(self):
        return f"<Server(id='{self.id}', name='{self.name}', ip='{self.ip}', fonction='{self.fonction}', nbr_cpu='{self.nbr_cpu}', RAM='{self.RAM}',disk='{self.disk})>"

def main():
    h1 = Server(name="SRV1", ip="10.0.0.1", fonction="Hyperviseur",nbr_cpu=64)
    print(h1)


if __name__ == "__main__":
    main()