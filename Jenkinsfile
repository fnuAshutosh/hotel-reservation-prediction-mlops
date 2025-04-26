pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }
    stages {
        // Stage 1: Clone Repository
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins...........' 
                    checkout scmGit(
                        branches: [[name: 'main']], 
                        userRemoteConfigs: [[
                            credentialsId: 'github-token', 
                            url: 'https://github.com/fnuAshutosh/hotel-reservation-prediction-mlops.git'
                        ]]
                    )
                }
            }
        }

        // Stage 2: Setup Environment
        stage('Setting up our virtual environment and installing dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and dependencies...' 
                    sh ''' 
                        python -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        pip install -e .
                    '''
                }
            }
        }
    }
}