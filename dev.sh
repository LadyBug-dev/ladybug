#!/bin/bash
# shellcheck disable=SC2181

init() {
    COMPOSE_EXECUTABLE="docker compose"
    $COMPOSE_EXECUTABLE version &>/dev/null
    if [[ $? -ne 0 ]]; then
        COMPOSE_EXECUTABLE="docker-compose"
        $COMPOSE_EXECUTABLE --version &>/dev/null
        if [[ $? -ne 0 ]]; then
            echo "Neither Docker Compose (plugin) or Docker-Compose (standalone) found, exitting!"
            exit 1
        fi
    fi
    self=$(which "$0")
    project_path=$(dirname "$self")
    compose_file_dist="${project_path}/docker-compose.yml"

    env_file="--env-file ${project_path}/.docker/.env"
    if [ -f "${project_path}/.docker/.env.local" ]; then
        env_file="${env-file} --env-file ${project_path}/.docker/.env.local"
    fi
    if [ -f "${project_path}/.docker/.local/.env" ]; then
        env_file="${env-file} --env-file ${project_path}/.docker/.local/.env"
    fi

    compose_file_custom="${project_path}/docker-compose.local.yml"
    if [ -f "${compose_file_custom}" ]; then
        compose_file="-f $compose_file_dist -f $compose_file_custom "
    else
        compose_file="-f $compose_file_dist"
    fi

    USERID="$(id -u)"
    export USERID
    GROUPID="$(id -g)"
    export GROUPID
    USER_TERM="$TERM"
    export USER_TERM
    USER_SHELL="$SHELL"
    export USER_SHELL
}

start() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file up -d "$@"
}

up() {
    start "$@"
}

stop() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file stop "$@"
}

status() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file ps
}

down() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file down "$@"
}

exec() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file exec "$@"
}

restart() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file restart "$@"
}

build() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file build "$@"
}

shell() {
  echo "$@"
    ${COMPOSE_EXECUTABLE} $compose_file $env_file run --rm --entrypoint "$SHELL" app -li "$@"
}

logs() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file logs "$@"
}

poetry() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file run -t --rm app poetry "$@"
}

compose() {
    ${COMPOSE_EXECUTABLE} $compose_file $env_file "$@"
}

init

"$@"