package __basePackage__.client.rest.impl;

import static com.global.rest.exception.enums.ErrorSource.HTTP_CLIENT_COMPONENT;
import static com.global.rest.exception.utils.RetrofitUtils.checkCallExecute;
import static com.global.rest.exception.utils.RetrofitUtils.checkResponse;

import __basePackage__.client.dto.__ApiName__RequestDto;
import __basePackage__.client.dto.__ApiName__ResponseDto;
import __basePackage__.client.mapper.__ApiName__RequestClientMapper;
import __basePackage__.client.mapper.__ApiName__ResponseClientMapper;
import __basePackage__.client.rest.__ApiName__Client;
import __basePackage__.client.rest.api.__ApiName__Api;
import __basePackage__.domain.external_request.__ApiName__Request;
import __basePackage__.domain.external_request.__ApiName__Response;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class __ApiName__ClientImpl implements __ApiName__Client {

  private final __ApiName__Api __apiName__Api;

  @Override
  public __ApiName__Response create__ApiName__(/* TODO: Add parameters */) {
    // TODO: Map domain request to DTO if needed
    // __ApiName__RequestDto requestDto = __ApiName__RequestClientMapper.INSTANCE.toDto(domainRequest);

    __ApiName__ResponseDto __apiName__ResponseDto =
        checkResponse(
            checkCallExecute(
                __apiName__Api.create__ApiName__(/* TODO: Pass parameters */),
                HTTP_CLIENT_COMPONENT),
            HTTP_CLIENT_COMPONENT);

    return __ApiName__ResponseClientMapper.INSTANCE.toModel(__apiName__ResponseDto);
  }
}
