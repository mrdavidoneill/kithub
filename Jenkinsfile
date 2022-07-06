import groovy.text.SimpleTemplateEngine

pipeline {
    agent any

    environment {
        DEVELOPMENT = true
        SECRET_KEY = credentials('SECRET_KEY')
        ALLOWED_HOSTS = credentials('ALLOWED_HOSTS')
        DB_ENGINE = 'django.db.backends.mysql'
        DB_HOST = 'db'
        DB_PORT = 3306
        DB_DATABASE = 'kithub'
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
        MARIADB_ROOT_PASSWORD = credentials('MARIADB_ROOT_PASSWORD')
        MARIADB_DATABASE = 'kithub'
        MARIADB_USER = credentials('MARIADB_USER')
        MARIADB_PASSWORD = credentials('MARIADB_PASSWORD')
        NGINX_HOST = 'localhost'
    }
    stages {
        stage('Setup .env') {
            steps {
                sh '''
                    echo $DB_HOST

                    '''
            }
        }
        stage('Unit test') {
            steps {
                sh 'env > .env'
                sh '''
                    docker-compose -f docker-compose-unittest.yml up --build --abort-on-container-exit

                    '''
            }
        }
    }
}
