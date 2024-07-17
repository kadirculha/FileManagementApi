from fastapi import FastAPI, HTTPException
from config.input_params import RequestItem
import uvicorn
from config.validation import InputValidate
from config.file_management import Director

app = FastAPI()

@app.post("/process_request")
async def process_request(item: RequestItem):
    """
    -
            {
            "eventType": "INSERT|UPDATE|DELETE",
            "companyId": 1234,
            "corridor": {
                "id": "uuid",
                "content": {
                "key": "value"
                }
            }
            }
    :param item:
    :return:
    """
    try:
        director = Director()
        validate = InputValidate()

        validate.validate(item=item)
        base_path, file_name = director.get_path(item=item)

        if item.eventType == "INSERT":
            director.write(base_path, file_name.strip(), item.corridor.content)
        elif item.eventType == "UPDATE":
            if director.check_file(base_path, file_name):
                director.write(base_path, file_name.strip(), item.corridor.content)
            else:
                raise ValueError(f"File {base_path}/{file_name} doesn't exist")
        elif item.eventType == "DELETE":
            director.delete(base_path, file_name)
        else:
            raise ValueError(f"Invalid eventType: {item.eventType}")

        return {"status": True, "message": "Request processed successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
