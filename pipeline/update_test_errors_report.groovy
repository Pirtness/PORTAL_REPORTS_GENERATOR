pipeline {
  agent {
    label "(Linux_Default || linux_slave || masterLin) && !tkle-jen0009"
  }
  options {
    timestamps()
    ansiColor('xterm')
    skipDefaultCheckout true
    timeout(time: 90, unit: 'MINUTES')
    buildDiscarder(logRotator(daysToKeepStr: '10', numToKeepStr: '10', artifactDaysToKeepStr: '10',
            artifactNumToKeepStr: '1'))
  }

  triggers {
    cron 'H/15 * * * *'
  }
  parameters {
    booleanParam defaultValue: false, description: '', name: 'UPDATE_PIPELINE'
  }

  stages {
    stage('run script') {
      when {
        expression {
          return !params.UPDATE_PIPELINE
        }
      }
      steps {
        script {
          tool name: 'ansible29py38', type: 'org.jenkinsci.plugins.ansible.AnsibleInstallation'
          sshagent(['user_ssh_git']) {
          withCredentials([usernamePassword(credentialsId: postgres_cred, passwordVariable: 'db_pass', usernameVariable: 'db_user'),
                           usernamePassword(credentialsId: dom_cred, passwordVariable: 'dom_pass', usernameVariable: 'dom_user')]) {
            withEnv(["db_user=${db_user}",
                     "db_pass=${db_pass}"]) {
              sh "sh run_script.sh update_test_errors_report.py"
              //sh "python3 -m venv ./venv && source ./venv/bin/activate && ./venv/bin/pip3 install -i http://mirror.sigma.sbrf.ru/pypi/simple --trusted-host mirror.sigma.sbrf.ru -r requirements.txt && python3 app.py && deactivate"
            }
          }
          }
        }
      }
    }
  }
  post {
    failure {
      zip archive: true, dir: '', glob: '*.log', zipFile: 'logs.zip'
    }
    always {
      cleanWs()
    }
  }
}