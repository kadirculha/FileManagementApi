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
                "content": null
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

        if item.eventType in ["UPDATE", "INSERT"]:
            director.write(base_path, file_name.strip(), item.corridor.content)
            return {"status": True, "message": "Request processed successfully"}
    
        elif item.eventType == "DELETE":
            delete_result = director.delete(base_path, file_name)
            return delete_result
        else:
            return {"status": False, "message": f"Invalid eventType: {item.eventType}"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, workers=1)