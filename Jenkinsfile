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
                def Url = "https://source.gtriip.com/scm/web_app/shippingcontainer_guest.git"
                git credentialsId: 'phuwai-bitbucket', url: Url
                sshagent (credentials: ['ssh-shippingcontainer']) {
                    sh '''
                        ssh -t phu@54.179.10.115 "cd GuestFacing/shippingcontainer_guest && 
                        git pull url && 
                        docker-compose pull &&
                        docker-compose up -d"
                    '''
                }
                
            }
        }
    }
}