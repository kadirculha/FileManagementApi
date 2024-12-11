from fastapi import FastAPI, HTTPException
from config.input_params import RequestItem
import uvicorn
from config.validation import InputValidate
from config.file_management import Director
import requests 
from loguru import logger

app = FastAPI()




def notify_ai_api(item : RequestItem):
    """
    AI API'yi bilgilendiren bir fonksiyon.

    :param event_type: Değişiklik türü (INSERT, UPDATE, DELETE)
    :param company_id: Şirket ID'si
    :param corridor_id: Corridor ID'si
    :param content: Corridor içeriği (DELETE için None olabilir)
    """
    # ai_api_url = "http://localhost:8090/webhook_update"  # AI API webhook URL'si
    ai_api_url = "http://3.69.36.239:8010/webhook_update" 
    # payload = {
    #     "eventType": item.eventType,
    #     "companyId": item.companyId,
    #     "corridor": {
    #         "id": item.corridor.id,
    #         "content": item.corridor.content
    #     }
    # }
    try:
        response = requests.post(ai_api_url, json=item.dict(), timeout=10)
        response.raise_for_status()
        logger.info(f"AI API'ye gönderildi: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.info(f"AI API'ye bildirim gönderilirken hata oluştu: {e}")

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
            # Corridor'u yaz
            director.write(base_path, file_name.strip(), item.corridor.content)
            
            # AI API'yi bilgilendir
            notify_ai_api(item)

            return {"status": True, "message": "Request processed successfully"}
    
        elif item.eventType == "DELETE":
            # Corridor'u sil
            delete_result = director.delete(base_path, file_name)
            
            # AI API'yi bilgilendir
            notify_ai_api(item)

            return delete_result
        else:
            return {"status": False, "message": f"Invalid eventType: {item.eventType}"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=False, workers=4)