pipeline {
    agent any
    options {
        checkoutToSubdirectory('rciam-service-registry-agent')
    }
    environment {
        PROJECT_DIR="rciam-service-registry-agent"
    }
    stages {
        stage ('Upload to PyPI') {
            when {
                branch 'master'
            }
            agent {
                docker {
                    image 'argo.registry:5000/python3'
                }
            }
            steps {
                echo 'Build python package'
                withCredentials(bindings: [usernamePassword(credentialsId: 'rciam-pypi-token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        cd ${WORKSPACE}/$PROJECT_DIR
                        pipenv install install setuptools twine wheel
                        pipenv run python3 setup.py sdist bdist_wheel
                        pipenv run python3 -m twine upload -u $USERNAME -p $PASSWORD dist/*
                    '''
                }
            }
            post {
                always {
                    cleanWs()
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}