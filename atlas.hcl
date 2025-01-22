data "external_schema" "sqlalchemy" {
    program = [
        "python3",
        "load_models.py"
    ]
}

env "postgresql" {
    src = data.external_schema.sqlalchemy.url

    # Добавяме search_path=public и exclude_schemas за _heroku
    dev = "postgresql://u4tsvphn6h9fmb:p701206212ecf586c814e68b9b9195894d9be79dff2732ddf37c5be005c002e42@clhtb6lu92mj2.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d1mbd270k9dkqn?search_path=public"
    url = "postgresql://u4tsvphn6h9fmb:p701206212ecf586c814e68b9b9195894d9be79dff2732ddf37c5be005c002e42@clhtb6lu92mj2.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d1mbd270k9dkqn"

    migration {
        dir = "file://migrations"
    }

    exclude_schemas = ["_heroku"]

    format {
        migrate {
            diff = "{{ sql . }}"
        }
    }
}