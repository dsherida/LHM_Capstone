package com.example.lhm_capstone;

import com.example.lhm_capstone.NextActivityFragment.NextActivityFragmentInteractionListener;

import android.R.string;
//import android.support.v7.app.ActionBarActivity;
//import android.support.v7.app.ActionBar;
import android.app.Fragment;
import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Build;

public class AssetDetailsFragment extends Fragment implements android.view.View.OnClickListener {
	private static final String ARG_PARAM1 = "param1";
	private static final String ARG_PARAM2 = "param2";
	
	AssetDetailsFragmentInteractionListener mListener;
	
	Button submitButton;
	Spinner spinnerStatus, spinnerOk, spinnerAction;
	TextView assetMakeName, assetModelName, assetVINID;
	CharSequence modelName, makeName, VinId;
	
	public static AssetDetailsFragment newInstance(String param1, String param2){
		AssetDetailsFragment fragment = new AssetDetailsFragment();
		Bundle args = new Bundle();
		args.putString(ARG_PARAM1, param1);
		args.putString(ARG_PARAM2, param2);
		fragment.setArguments(args);
		return fragment;
	}
	
	public AssetDetailsFragment(){
		// Required empty public constructor
	}
	
	
    @Override
	public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setContentView(R.layout.activity_asset_details);

        /*
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.content_view, new PlaceholderFragment())
                    .commit();
        }
        */
        /*
        assetMakeName = (TextView)findViewById(R.id.assetMakeName);
        assetMakeName.append(makeName);
        assetModelName = (TextView)findViewById(R.id.assetModelName);
        assetModelName.append(modelName);
        assetVINID = (TextView)findViewById(R.id.assetVINID);
        assetVINID.append(VinId);
        */
    }
    
    @Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
    	// Set onClickListener to the go_button
		View view = inflater.inflate(R.layout.fragment_asset_details, container, false);
		submitButton = (Button) view.findViewById(R.id.submit_button);
		submitButton.setOnClickListener(this);
		
		// Inflate the layout for this fragment
		return view;
	}
    
    @Override
	public void onAttach(Activity activity) {
		super.onAttach(activity);
		try {
			mListener = (AssetDetailsFragmentInteractionListener) activity;
		} catch (ClassCastException e) {
			throw new ClassCastException(activity.toString()
					+ " must implement AssetDetailsFragmentInteractionListener");
		}
	}
    
    @Override
	public void onDetach() {
		super.onDetach();
		mListener = null;
	}
    
    public interface AssetDetailsFragmentInteractionListener {
		public void submitButtonClicked();
	}

    /*
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.asset_details, menu);
        return true;
    }*/

    /*
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
    */
    
    public void sendMessage(View view)
    {
    	//update database with spinner selections and link to next activity
    	//not really sure how to do it, but leaving this here for now
    }

	@Override
	public void onClick(View arg0) {
		// TODO Auto-generated method stub
		Toast.makeText(this.getActivity(), "Submitting...", Toast.LENGTH_LONG).show();
        mListener.submitButtonClicked();
		
	}

}
