from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_



'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture(scope="module")
def create_orders():
    created_ids = []

    response = api_helpers.post_api_data("/store/order", {
        "pet_id": 2,
    })
    
    created_ids.append(response.json()["id"])
        

    yield  created_ids

    for oid in created_ids:
        api_helpers.delete_api_data(f"/store/{oid}", oid)


@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_patch_order_by_id(create_orders, status):
    order_id = create_orders[0]
    test_endpoint = f"/store/order/{order_id}"
    param = {
        "status": status
    }

    response = api_helpers.patch_api_data(test_endpoint, param)
    print(response.status_code)
    print(response.text)    
    data = response.json()
    response.status_code == 200
    assert data["message"] == "Order and pet status updated successfully"