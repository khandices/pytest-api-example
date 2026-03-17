from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
from app import PET_TYPE, PET_STATUS


'''
Creating dummy data here with fixture
Ideally, I would spin up test db instance that would have test db data.
This is typically done to ensure that no real data is being tested on.
For this tech challenge, however, 
I'm adding test data and then cleaning it up afterward.
'''
@pytest.fixture(scope="module")
def create_pets():
    created_ids = []

    for i in range(3):
        response = api_helpers.post_api_data("/pets", {
            "id" : i + 100,
            "name": f"test_pet_{i+1}",
            "type": PET_TYPE[i],
            "status": PET_STATUS[i]
        })
        created_ids.append(response.json()["id"])

    yield  

    for pet_id in created_ids:
        api_helpers.delete_api_data(f"/pets/{pet_id}", pet_id)



'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''

def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "sold", "pending" ])
def test_find_by_status_200(status, create_pets):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    
    assert response.status_code == 200
    data = response.json()

    # Doing this to ensure I'm only accessing test data
    # My workaround for not having a test db instance
    test_data = [pet for pet in data if pet["name"].startswith("test_pet_")]

    for pet in test_data:
        assert pet["status"] == status
        validate(instance=pet, schema=schemas.pet)

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''

@pytest.mark.parametrize("pet_id", [3000, -10, "kha", 1.5])
def test_get_by_id_404(pet_id):
    
    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404