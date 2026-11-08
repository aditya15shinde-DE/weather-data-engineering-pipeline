from numbers import Real

def validate_weather(data):
    """
    Validate the structure and essential values of a weather API rsponse.

    Returns:
        (True, []) if valid.
        (False, errors) if invalid.
    """


    errors = []

    # 1. Check that response is dictionary
    if not isinstance(data,dict):
        return False, ["Weather response must be dictionary"]

    # 2. Validate City Name
    city = data.get("name")

    if not isinstance(city,str) or not city.strip():
        errors.append("City name is missing or invalid")

    # 3. Validate the main weather section
    main = data.get("main")
    if not isinstance(main,dict):
        errors.append("Main weather section is invalid or missing")

    else:
        #Temperature must be numeric
        temperature = main.get("temp")

        if (
            isinstance(temperature,bool)
            or not isinstance(temperature,Real)

        ):
            errors.append("Temperature is missing or not numeric")

        # Humidity must be numeric and between 0 and 100
        humidity=main.get("humidity")

        if(
            isinstance(humidity,bool)
            or not isinstance(humidity,Real)
        ):
            errors.append("Humidity is missing or not numeric")

        elif not 0 <= humidity <=100:
            errors.append("Humidity must be between 0 and 100")

    # 4. Validate the observation timestamp
    timestamp=data.get("dt")
    if(
        isinstance(timestamp,bool)
        or not isinstance(timestamp,int)
        or timestamp<=0
    ):
        errors.append("Observation timestamp is missing or invalid")

    return len(errors)==0,errors

    