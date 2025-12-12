package __basePackage__.client.mapper;

import __basePackage__.client.dto.__ApiName__RequestDto;
import __basePackage__.domain.external_request.__ApiName__Request;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface __ApiName__RequestClientMapper {
    __ApiName__RequestClientMapper INSTANCE = Mappers.getMapper(__ApiName__RequestClientMapper.class);

    __ApiName__RequestDto toDto(__ApiName__Request __apiName__Request);
}
