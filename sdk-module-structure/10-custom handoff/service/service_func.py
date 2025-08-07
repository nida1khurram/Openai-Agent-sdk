
from agents import RunContextWrapper
from input_schema.input_schema import MyInputData

async def service(ctx:RunContextWrapper, input_data:MyInputData):
    print(ctx.context)
    print("reason->:",input_data.reason)    #input print