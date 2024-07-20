from config.input_params import RequestItem


class InputValidate:
    def __init__(self):
        pass

    def validate(self, item: RequestItem):
        item_dict = item.dict()

        eventTypes = ["INSERT", "UPDATE", "DELETE"]

        # validate eventType
        if not isinstance(item_dict.get("eventType"), str):
            raise ValueError("eventType should be a string")
        if item_dict.get("eventType") not in eventTypes:
            raise ValueError(f"eventType should be one of {eventTypes}")

        # validate companyId
        if not isinstance(item_dict.get("companyId"), int):
            raise ValueError("companyId should be an integer")

        # validate corridor_id
        if not isinstance(item_dict.get("corridor").get("id"), str):
            raise ValueError("corridor.id should be a string")

        # # validate corridor.content
        # if not isinstance(item_dict.get("corridor").get("content"), dict):
        #     raise ValueError("corridor.content should be a dict")

        # if not item_dict.get("corridor").get("content"):
        #     raise ValueError("corridor.content field cannot be empty")
