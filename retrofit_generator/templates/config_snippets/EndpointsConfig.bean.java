
  @Bean
  @ConfigurationProperties(prefix = "http-client.__serviceIdentifier__")
  public Endpoint __apiName__Endpoint() {
    return new Endpoint();
  }
