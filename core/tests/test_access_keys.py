import pytest
from rest_framework import status
from model_bakery import baker
from core.models import AccessKey, School


@pytest.mark.django_db
class TestGenerateNewAccessKey():
    def test_if_school_is_not_authenticated_return_401(self, api_client):
        response = api_client.post('/api/v1/keys/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
                
    
    def test_if_school_is_authenticated_return_201(self, api_client, authenticate):
        authenticate()
        response = api_client.post('/api/v1/keys/')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'active'
        
    
    def test_if_school_is_authenticated_and_has_active_key_return_400(self,api_client,authenticate):
        authenticate()
        school = baker.make(School)
        baker.make(AccessKey, school=school, status='active')
        respose = api_client.post(f'/api/v1/schools/{school.id}/keys/')
        assert respose.status_code == status.HTTP_400_BAD_REQUEST
        assert respose.data['error'] == 'School already has an active key'
       


@pytest.mark.django_db
class TestListAccessKeys():
    def test_if_school_is_not_authenticated_return_401(self, api_client):
        response = api_client.get('/api/v1/keys/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_if_school_is_authenticated_but_not_admin_return_200(self, api_client, authenticate):
        authenticate()
        response = api_client.get('/api/v1/keys/')
        assert response.status_code == status.HTTP_200_OK
    
    
    def test_if_school_is_admin_return_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        school_A = baker.make(School)
        school_B = baker.make(School)
        baker.make(AccessKey, school=school_A)
        baker.make(AccessKey, school=school_B)
        response = api_client.get('/api/v1/keys/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
        
    


@pytest.mark.django_db
class TestDeleteAccessKey():
    def test_if_school_is_not_authenticated_return_401(self, api_client):
        response = api_client.delete('/api/v1/keys/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_if_school_is_authenticated_but_not_admin_return_403(self, api_client, authenticate):
        authenticate()
        response = api_client.delete('/api/v1/keys/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    def test_if_school_is_admin_return_405(self, api_client, authenticate):
        authenticate(is_staff=True)
        access_key = baker.make(AccessKey)
        response = api_client.delete(f'/api/v1/keys/{access_key.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        



@pytest.mark.django_db
class TestUpdateAccessKey():
    def test_if_school_is_not_authenticated_return_401(self,api_client):
        data = {'status':'revoke'}
        response = api_client.patch(f'/api/v1/keys/1/',data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_if_school_is_authenticated_but_not_admin_return_403(self,api_client,authenticate):
        authenticate()
        data = {'status':'revoke'}
        response = api_client.patch(f'/api/v1/keys/1/',data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    def test_if_school_is_authenticated_and_admin_return_200(self,api_client,authenticate):
        authenticate(is_staff=True)
        access_key = baker.make(AccessKey)
        data = {'status':'revoke'}
        response = api_client.patch(f'/api/v1/keys/{access_key.id}/',data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        
        

@pytest.mark.django_db
class TestRevokeAccessKey():
    def test_if_school_is_not_authenticated_return_401(self,api_client):
        response = api_client.post('/api/v1/keys/1/revoke/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
    def test_if_school_is_authenticated_but_not_admin_return_403(self,api_client,authenticate):
        authenticate()
        response = api_client.post('/api/v1/keys/1/revoke/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    
    def test_if_school_is_authenticated_and_admin_return_200(self,api_client,authenticate):
        authenticate(is_staff=True)
        access_key = baker.make(AccessKey)
        response = api_client.post(f'/api/v1/keys/{access_key.id}/revoke/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'revoked'