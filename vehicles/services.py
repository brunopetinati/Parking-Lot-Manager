from parking.models import ParkingModel

# verifica se existe vaga no nível
# filtra se no nível existe vaga de variedade = tipo do veículo, ordenada por id.
# caso encontre, retorna a primeira vaga[0] 

def has_parking_by_type(floor, vehicle_type):

    # vehiclemodel = model, verificar


    available_spaces = floor.spacemodel_set.filter(
        variety=vehicle_type, vehiclemodel=None
    ).order_by('id')

    if available_spaces:
        return available_spaces[0]
    return None

# verifica se há vaga em algum outro nível (ou em outros níveis/andares)
# o sinal de menos indica do menor para o maior, ordem crescente 

def find_paking_all(vehicle_type):
    floors_by_priority = ParkingModel.objects.order_by('-fill_priority')

    # para cada nível, checa com a função de cima, se há vaga
    for floor in floors_by_priority:
        space = has_parking_by_type(floor, vehicle_type)
        if space:
            return space
        else:
            continue

    return None