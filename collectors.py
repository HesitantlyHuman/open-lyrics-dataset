import asyncio

#Check that this works with StopIteration from interface
async def collection_worker(interface, data_partitioner):
    while True:
        data = await next(interface)
        data_partitioner.append(data)
        data_partitioner.update_index(interface.index)