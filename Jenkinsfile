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
        DOCKER_REGISTRY = 'mrdavidoneill'
        SERVICE = 'kithub-api'
        TAG = '1.0.0'
    }
    stages {
        stage('Setup test .env') {
            steps {
                sh 'env > .env'
            }
        }

        stage('Build test image') {
            steps {
                sh """
                    docker buildx build . -t $DOCKER_REGISTRY/$SERVICE:test
                    """
            }
        }

        stage('Unit test') {
            steps {
                sh '''
                    docker-compose -f docker-compose-unittest.yml up --abort-on-container-exit

                    '''
            }
        }
        stage('System test') {
            steps {
                sh '''
                    docker-compose -f docker-compose-systemtest.yml up --abort-on-container-exit

                    '''
            }
        }
        stage('Acceptance test') {
            steps {
                sh '''
                    docker-compose -f docker-compose-acceptancetest.yml up --abort-on-container-exit

                    '''
            }
        }

        stage('Push image') {
            environment {
                DOCKER_USERNAME = credentials('DOCKER_USERNAME')
                DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
            }
            steps {
                sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'

                sh """
                    docker buildx build --platform=linux/arm64 . --push -t $DOCKER_REGISTRY/$SERVICE:$TAG -t $DOCKER_REGISTRY/$SERVICE:latest
                    """
            }
        }

        stage('Setup production .env') {
            environment {
                DEVELOPMENT = false
                ALLOWED_HOSTS = 'api.raspberrypi'
                NGINX_HOST = 'raspberrypi'
            }
            steps {
                sh 'env > production.env'
            }
        }

        stage('Deploy API') {
            environment {
                ansible_vault_password = credentials('ANSIBLE_VAULT_PASSWORD')
            }
            steps {
                ansiblePlaybook(vaultCredentialsId: 'ANSIBLE_VAULT_PASSWORD_FILE', inventory: 'ansible/hosts',
                playbook: 'ansible/api.yml', disableHostKeyChecking: true)
            }
        }
    }
}
