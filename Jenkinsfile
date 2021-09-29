pipeline { 
    agent any 
    
    stages {
        stage('Get Latest Code') { 
            steps { 
                checkout scm 
            }
        }
        stage('Deploy'){
            steps {
                echo 'Deploying.....'
                sshagent (credentials: ['ssh-jenkinstest']) {
                    sh 'pwd'
                    sh 'scp -r /var/jenkins_home/workspace/web/sc-guestfacing/* phu@18.141.54.154:/home/phu/shippingcontainer_guest'
                    sh '''
                        ssh -tt -o StrictHostKeyChecking=no phu@18.141.54.154 "cd shippingcontainer_guest &&
                        ls &&
                        docker-compose down &&
                        docker-compose build &&
                        docker image prune -f &&
                        docker-compose up -d"
                    '''
                }
                
            }
        }
    }
}