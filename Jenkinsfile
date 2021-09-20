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
                sshagent (credentials: ['ssh-shippingcontainer']) {
                    sh 'ls'
                    sh 'scp -R /var/jenkins_home/workspace/shippingconatiner-guestfacing@3 phu@54.179.10.115:/home/phu/GuestFacing/shippingconatiner_guest'
                    sh '''
                        ssh -t phu@54.179.10.115 "cd GuestFacing/shippingcontainer_guest &&  
                        docker-compose pull &&
                        docker-compose up -d"
                    '''
                }
                
            }
        }
    }
}