# Implementation of DCR (Data Clean Room)

## Secure Multiparty Data Sharing with Confidential Computing

Data Clean Rooms provide a secure space for companies to collaborate on data analysis without revealing private user information.
Ideal for scenarios where multiple parties need to combine data for better insights.
Publishers and advertisers can improve ad targeting while maintaining user privacy.
By anonymizing data within a controlled environment, Data Clean Rooms reduce privacy risks and ensure compliance with regulations.
This approach allows for richer data analysis and more accurate models.
While keeping user data confidential, companies can gain valuable insights.
Data Clean Rooms strike a balance between data utility and privacy.
Enabling collaboration and innovation while respecting user trust.

Confidential computing uses Trusted Execution Environments (TEEs) like Intel® TDX and SGX to create secure enclaves within processors. 
These enclaves protect data confidentiality and integrity, even if the system is compromised.
Imagine a locked vault inside your computer for processing sensitive information.
This technology is ideal for Virtual Machines (VMs), enabling secure data processing on shared hardware.
It's like having multiple secure computers running on one physical machine.
Secure enclaves ensure your data remains protected throughout processing.

Confidential computing relies on Trusted Execution Environments (TEEs) built into modern processors like Intel® SGX and TDX. These TEEs act like secure vaults within the processor, protecting data confidentiality and integrity even in a compromised system.

Here's how to achieve confidential computing:
- Leverage cloud platforms or hardware that supports TEEs.
- Develop your application to utilize TEE libraries (e.g., Intel SGX SDK).
- Design your code to process sensitive data within the secure TEE enclave.
- TEEs handle computations, keeping your data encrypted and isolated from the rest of the system.

Cloud Confidential VMs offer a simpler approach to confidential computing compared to local setups. Here's why:

- Pre-configured Environment: Cloud providers manage the TEE infrastructure, eliminating the need for local installation and configuration of TEE libraries.
- Scalability and Flexibility: Cloud VMs offer easy scaling based on your needs, while local setups might require additional hardware investment.
- Security Expertise: Cloud providers have expertise in securing their infrastructure, potentially enhancing overall security compared to a local environment.
While local setups offer more control, cloud Confidential VMs provide a quicker and potentially more secure option for leveraging TEEs.

Using Azure Cloud Confidential VM ?
- Pre-built Security: Utilize pre-configured VMs with built-in TEE (Trusted Execution Environment) technology like Intel SGX or AMD SEV-SNP.
- Simple Setup: Skip local TEE library installation and configuration complexities.
- Secure Enclave: Isolate sensitive data processing within the secure enclave of the TEE, protecting confidentiality and integrity.
- Scalability: Easily scale your resources up or down as needed based on your workload.
- Cloud Expertise: Benefit from Microsoft's security expertise for a potentially more secure environment.


Azure confidential virtual machines FAQ about is security and confidentiality.
- https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-vm-faq

Choose a Confidential VM offering: Azure offers various Confidential VM configurations with Intel SGX or AMD SEV-SNP support. Select a VM size that meets your processing needs and budget.

### Create a Cloud Confidential VM:

Azure Portal:
- Navigate to the "Virtual Machines" service in the Azure portal.
- Click "Add" to create a new VM.
- Select your chosen Confidential VM offering and configure settings like size, storage, and networking.
- During configuration, enable features like "Trusted Launch" or "Secure Enclave" depending on the chosen TEE technology (SGX or SEV-SNP).

Configure Network Security:
- Implement security groups on your VM to restrict inbound and outbound traffic, ensuring only authorized communication occurs.

Install Software:
- Connect to your Azure VM using Remote Desktop or SSH.
- Install the necessary software stack for your data clean room functionality. This might include:
- Python and data science libraries (Pandas, scikit-learn) for data handling and anonymization.
- TEE libraries specific to your chosen technology (Intel SGX SDK or AMD SEV libraries) for secure data processing within the enclave.
- Containerization tools like Docker to package your application components for easier management.

### Using Docker Containers:

- Isolation: Docker containers provide additional isolation for your data clean room application, further enhancing security.
- Portability: Docker images package your application and its dependencies, simplifying deployment across different environments.
- Resource Management: Containers share the underlying operating system of the VM, optimizing resource utilization.


#### Setup Docker 

```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Install docker pkg's

```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Container Image Development:

Develop Docker images that encapsulate your data clean room functionalities.
These images can include:
Your application code for data preprocessing, model training, and analysis.
Libraries like Pandas, scikit-learn, and SMPC libraries (e.g., SCALE-ML, PySyft) for data manipulation and privacy-preserving computations.
TEE libraries (e.g., Intel SGX SDK) to interact with the secure enclave for sensitive data processing.
Consider using multi-stage builds to optimize the final image size.

[Docker_Image](./Dockerfile)

#### Setup Tools
```sh
sudo apt install tpm2-tools -y
```
#### Create Endorsement Key (EK)
Initialize the TPM by creating an Endorsement Key:
```sh
tpm2_createek --ek-context rsa_ek.ctx --key-algorithm rsa --public rsa_ek.pub
```
#### Create Attestation Key (AK)
Create an Attestation Key derived from the EK, used for signing quotes and attestations:
```sh
tpm2_createak \
   --ek-context rsa_ek.ctx \
   --ak-context rsa_ak.ctx \
   --key-algorithm rsa \
   --hash-algorithm sha256 \
   --signing-algorithm rsassa \
   --public rsa_ak.pub \
   --private rsa_ak.priv \
   --ak-name rsa_ak.name
```
####  Save the AK's Public Key
Save the Attestation Key's public key from each confidential VM into a remote key/attestation server for future verification.

### PCR
Platform Configuration Registers (PCRs) are unique elements within the TPM2 that can only be updated using a hashing mechanism. This one-way update process guarantees the integrity of your code.

#### Initialize PCR
First, read the PCR values to establish a baseline:

#### Extending values into PCR
first we need to hash the data, then extend it to PCR
```sh
tpm2_pcrread sha1:0,1,2+sha256:0,1,2
```

---

Sources