# Sequential full re-run on the current machine. No competing inference jobs.
$py = '.\.venv\Scripts\python.exe'
$sets = @{ dev='datasets/manifest.json'; holdout='datasets/holdout.json'; fresh='datasets/phase1c/validation.json' }
$configs = @(
  @{ name='gpu-directml'; args=@('--backend','directml','--device-id','1','--threads','8') },
  @{ name='cpu-32t';      args=@('--backend','opencv','--threads','32') },
  @{ name='cpu-2t';       args=@('--backend','opencv','--threads','2') }
)
foreach ($c in $configs) { foreach ($k in $sets.Keys) {
  Write-Host "=== $($c.name) / $k"
  & $py -m evaluation.run --manifest $sets[$k] --output "evaluation/rtx5060/$($c.name)/$k" @($c.args)
}}
