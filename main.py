from fastapi import FastAPI
from keystone import *
from pydantic import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

class DiasmRequest(BaseModel):
    arch: str
    mode: str
    code: str

ks_arch_dict = {
    "X86": KS_ARCH_X86,
    "ARM": KS_ARCH_ARM,
    "ARM64": KS_ARCH_ARM64,
    "EVM": KS_ARCH_EVM,
    "MIPS": KS_ARCH_MIPS,
    "PPC": KS_ARCH_PPC,
    "SPARC": KS_ARCH_SPARC
}

ks_mode_dict = {
    "X16": KS_MODE_16,
    "X32": KS_MODE_32,
    "X64": KS_MODE_64,
    "ARM": KS_MODE_ARM,
    "THUMB": KS_MODE_THUMB,
    "MICRO": KS_MODE_MICRO,
    "MIPS3": KS_MODE_MIPS3,
    "MIPS32R6": KS_MODE_MIPS32R6,
    "V8": KS_MODE_V8,
    "V9": KS_MODE_V9,
    "QPX": KS_MODE_QPX
}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/disasm/")
async def disasm(request: DiasmRequest):
    logger.info(f"Received disasm request: {request}")
    try:
        ks = Ks(ks_arch_dict[request.arch], ks_mode_dict[request.mode])
        encoding, count = ks.asm(request.code)
        logger.info(f"Disassembly successful: encoding={encoding}, count={count}")
        return {"encoding": encoding, "count": count}
    except Exception as e:
        logger.error(f"Disassembly failed: {e}")
        return {"error": str(e)}

@app.get("/diasm/archs")
async def get_archs():
    return {"archs": list(ks_arch_dict.keys())}

@app.get("/diasm/modes")
async def get_modes():
    return {"modes": list(ks_mode_dict.keys())}