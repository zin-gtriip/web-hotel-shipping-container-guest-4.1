pipeline { 
    agent any 
    
    stages {
        stage('Get Latest Code') { 
            steps { 
                checkout scm 
            }
        }
        stage('Deploy'){
            environment {
                GIT_CREDS = credentials('phuwai-bitbucket')
            }
            steps {
                echo 'Deploying.....'

                git credentialsId: 'phuwai-bitbucket', url: 'https://$GIT_CREDS_USR:$GIT_CREDS_PSW@source.gtriip.com/scm/web_app/shippingcontainer_guest.git'
                sh 'ls'

                sshagent (credentials: ['ssh-jenkinstest']) {
                    sh 'pwd'
                    sh '''
                        ssh -tt -o StrictHostKeyChecking=no phu@18.141.54.154 "cd shippingcontainer_guest &&
                        ls &&
                        pwd &&
                        echo url &&
                        git pull url &&
                        docker-compose down &&
                        docker-compose build &&
                        docker image -y prune &&
                        docker-compose up -d"
                    '''
                }
                
            }
        }
    }
}