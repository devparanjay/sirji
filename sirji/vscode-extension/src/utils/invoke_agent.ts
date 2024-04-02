import * as childProcess from 'child_process';
import * as vscode from 'vscode';

export async function invokeAgent(scriptPath: string, args: string[] = []): Promise<any> {
 console.log('Executing command:', 'python3', [scriptPath, ...args].join(' '));
 const response = await executePythonScript(scriptPath, args);
 console.log(response);
 return response;
}

async function executePythonScript(scriptPath: string, args: string[] = []): Promise<any> {
 return new Promise((resolve, reject) => {
  const process = childProcess.spawn('python3', [scriptPath, ...args]);

  let responseData = '',
   errorData = '';

  process.stdout.on('data', (data) => {
   responseData += data.toString();
  });

  process.stderr.on('data', (data) => {
   errorData += data.toString();
  });

  process.on('error', (error) => {
   vscode.window.showErrorMessage(`Sirji> Python script execution error: ${error.message}`);
   reject(error);
  });

  process.on('close', (code) => {
   if (code === 0) {
    resolve(responseData);
   } else {
    if (errorData) {
     vscode.window.showErrorMessage(`Sirji> Python script execution error: ${errorData}`);
    }
    reject(new Error(`script exited with code ${code}`));
   }
  });
 });
}
