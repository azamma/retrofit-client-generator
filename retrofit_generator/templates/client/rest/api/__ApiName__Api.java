package __basePackage__.client.rest.api;

import __basePackage__.client.dto.__ApiName__ResponseDto;
import retrofit2.Call;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface __ApiName__Api {

  @Headers("Accept: application/json")
  @POST("__endpointPath__")
  Call<__ApiName__ResponseDto> create__ApiName__(/* TODO: Add parameters - e.g., @Header("Authorization") String token, @Body RequestDto body, @Query("param") String param */);
}
