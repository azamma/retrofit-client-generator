package __basePackage__.client.mapper;

import __basePackage__.client.dto.__ApiName__ResponseDto;
import __basePackage__.domain.external_request.__ApiName__Response;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface __ApiName__ResponseClientMapper {
    __ApiName__ResponseClientMapper INSTANCE = Mappers.getMapper(__ApiName__ResponseClientMapper.class);

    __ApiName__Response toModel(__ApiName__ResponseDto __apiName__ResponseDto);
}
