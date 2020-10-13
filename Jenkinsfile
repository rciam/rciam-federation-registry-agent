pipeline {
    agent any
    options {
        checkoutToSubdirectory('rciam-federation-registry-agent')
    }
    environment {
        PROJECT_DIR="rciam-federation-registry-agent"
    }
    stages {
        stage ('Upload to PyPI') {
            agent {
                docker {
                    image 'argo.registry:5000/python3'
                }
            }
            steps {
                echo 'Build python package'
                sh '''
                    cd ${WORKSPACE}/$PROJECT_DIR
                    pipenv install install setuptools twine wheel
                    pipenv run python3 setup.py sdist bdist_wheel
                '''
                script {
                    if ( env.BRANCH_NAME == 'master' ) {
                        withCredentials(bindings: [usernamePassword(credentialsId: 'rciam-pypi-token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                            sh '''
                                pipenv run python3 -m twine upload -u $USERNAME -p $PASSWORD dist/*
                            '''
                        }
                    }
                    if ( env.BRANCH_NAME == 'devel' ) {
                        withCredentials(bindings: [usernamePassword(credentialsId: 'rciam-test-pypi-token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                            sh '''
                                pipenv run python3 -m twine upload --repository testpypi -u $USERNAME -p $PASSWORD dist/*
                            '''
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
    }
    post {
        always {
            cleanWs()
        }
    }
}