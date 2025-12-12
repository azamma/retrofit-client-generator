
  @Bean
  public __ApiName__Api __apiName__Api(EndpointsConfig.Endpoint __apiName__Endpoint, OkHttpClient okHttpClient) {
    return createRestClient(__ApiName__Api.class, __apiName__Endpoint, okHttpClient);
  }
